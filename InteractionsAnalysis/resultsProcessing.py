from os.path import isdir
from openbabel import pybel
import pandas as pd
import os
from biopandas.pdb import PandasPdb
import spyrmsd
from Utilities.utils import checkFilesExistance, checkRMSDCorrectness
from config import Config
import json
from spyrmsd import io, rmsd
from statistics import fmean
import numpy as np


def getGninaDockingResult(filepath, return_df=True):
    scores = []
    for mol in pybel.readfile('sdf', filepath):
        # keys: minimizedAffinity, CNNscore, CNNaffinity, CNN_VS, CNNaffinity_variance
        scores.append({'title': mol.title, 
        'CNNscore': float(mol.data['CNNscore']),
        'CNNaffinity': float(mol.data['CNNaffinity']),
        'minimizedAffinity': float(mol.data['minimizedAffinity'])
        })
    
    if return_df:
        scores = pd.DataFrame(scores)
    return scores


def getGninaDockingResultFromPDBQT(filepath):
    # build a function to extract gnina output parameters from REMARK in header pdbqt file
    with open(filepath, "r") as pdb_reader:

        for l_no, line in enumerate(pdb_reader):
            line = line.replace("REMARK", "").split(" ")
            chunks = [word for word in line if word]
            if "minimizedAffinity" in chunks:
                break
            
    
    return {
        'minimizedAffinity': float(chunks[1]),
        'CNNscore': float(chunks[3]),
        'CNNaffinity': float(chunks[5])    
    }
                

def getVinaDockingResultFromPDBQT(filepath):
    with open(filepath, "r") as pdb_reader:

        for l_no, line in enumerate(pdb_reader):
            line = line.split(" ")
            chunks = [word for word in line if word]
            if "REMARK" in chunks:
                break    

    return {'affinity': float(chunks[3])}



def processGninaResultsByReceptor(receptor_folder):
    scores = []
    ligands = []
    for root, dirs, files in os.walk(receptor_folder):
        for file in files:
            if file == "out.pdbqt":
                
                try:
                    results = getGninaDockingResultFromPDBQT(os.path.join(root, file))
                    scores.append(results)
                except AttributeError:
                    continue
                ligands.append(os.path.join(root, file).split(os.sep)[-2])
    df = pd.DataFrame(scores)          
    return df

def averageGninaResults(df):
    record = {
        'CNNscore': fmean(df['CNNscore']),
        'CNNaffinity':fmean(df['CNNaffinity']),
        'minimizedAffinity': fmean(df['minimizedAffinity'])
    }
    return record

def averageVinaResults(df):
    record = {
        'affinity': fmean(df['affinity'])
    }
    return record

def processGninaResults(gnina_folder=Config.GNINA_DOCKING_FOLDER):
    scores = []
    receptors = []
    for dir in os.listdir(gnina_folder):
        if not os.path.isdir(os.path.join(gnina_folder, dir)):
            continue
        try:
            receptor_df = processGninaResultsByReceptor(os.path.join(gnina_folder, dir))
            record = averageGninaResults(receptor_df)
            record['code'] = str(dir)
            scores.append(record)
        except AttributeError:
            continue
        receptors.append(dir)

    df = pd.DataFrame(scores)
    return df

def processVinaResultsByReceptor(receptor_folder):
    scores = []
    ligands = []
    for root, dirs, files in os.walk(receptor_folder):
        for file in files:
            if file == "out.pdbqt":
                
                try:
                    results = getVinaDockingResultFromPDBQT(os.path.join(root, file))
                    scores.append(results)
                except AttributeError:
                    continue
                ligands.append(os.path.join(root, file).split(os.sep)[-2])
    df = pd.DataFrame(scores)          
    return df

def processVinaResults(vina_folder=Config.VINA_DOCKING_FOLDER):
    scores = []
    receptors = []
    for dir in os.listdir(vina_folder):
        if not os.path.isdir(os.path.join(vina_folder, dir)):
            continue
        try:
            receptor_df = processVinaResultsByReceptor(os.path.join(vina_folder, dir))
            record = averageVinaResults(receptor_df)
            record['code'] = str(dir)
            scores.append(record)
        except AttributeError:
            continue
        receptors.append(dir)

    df = pd.DataFrame(scores)
    return df


def compareRMSDs(ref_path, dock_results, verbose=True):
    # read ligand
    ref = io.loadmol(ref_path)
    
    # remove hydrogen atoms
    ref.strip()

    coords_ref = ref.coordinates
    anum_ref = ref.atomicnums
    adj_ref = ref.adjacency_matrix

    means = []
    for result in dock_results:
        # read docking results
        mols = io.loadallmols(result)
        
        for mol in mols:
            mol.strip()
   
        coords = [mol.coordinates for mol in mols]
        anum = mols[0].atomicnums
        adj = mols[0].adjacency_matrix

        try:
            # calculate Symmetric-Corrected RMSD
            RMSD = rmsd.symmrmsd(
                coords_ref,
                coords,
                anum_ref,
                anum,
                adj_ref,
                adj,
                minimize=True
            )
            means.append(fmean(RMSD))
        except spyrmsd.exceptions.NonIsomorphicGraphs:
            if verbose: print("WARNING: spyrmsd.exceptions.NonIsomorphicGraphs: Graphs are not isomorphic.")
            continue
    return means


def RMSDComparison(receptor, ligands_folder=Config.LIGANDS_SDF_FOLDER, docking_folders=[Config.VINA_DOCKING_FOLDER, Config.GNINA_DOCKING_FOLDER], verbose=True):
    
    means_list = []
    for root, dirs, files in os.walk(ligands_folder):
        for ligand in files:
            if not ligand.endswith(".sdf") or not ligand.startswith("ligand_"):
                continue

            # select corresponding docking results
            lig = ligand[ligand.find("_")+1:-4]

            docking_results = []
            for dock_folder in docking_folders:
                docking_results.append(os.path.join(dock_folder, str(receptor) + str(os.sep) + str(lig) + str(os.sep) + "out.pdbqt"))
                
            if not checkFilesExistance(docking_results):
                if verbose: print(f"WARNING: cannot compute RMSDs for {lig} because docking results don't exist!\n")
                continue
            
            rmsd = compareRMSDs(os.path.join(root, ligand), docking_results, verbose)
            if verbose: print(f"ligand: {lig}\nRMSDs [Vina, GNINA]: {rmsd}\n\n")
            if not checkRMSDCorrectness(rmsd):
                continue
            means_list.append(rmsd)
    
    means_matrix = np.array(means_list, dtype=object)
    results = np.mean(means_matrix, axis=0)
    return [results]