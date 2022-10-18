from openbabel import pybel
import pandas as pd
import os
from Utilities.utils import checkFilesExistance, checkRMSDCorrectness
from config import Config
import json
from spyrmsd import io, rmsd
from statistics import fmean
import numpy as np


def processDockingResult(filepath):
    scores = []
    for mol in pybel.readfile('sdf', filepath):
        # keys: minimizedAffinity, CNNscore, CNNaffinity, CNN_VS, CNNaffinity_variance
        scores.append({'title': mol.title, 
        'CNNscore': float(mol.data['CNNscore']),
        'CNNaffinity': float(mol.data['CNNaffinity']),
        'Vinardo': float(mol.data['minimizedAffinity']),
        'CNN_VS': float(mol.data['CNN_VS']),
        'CNNaffinity_variance': float(mol.data['CNNaffinity_variance'])})

    scores = pd.DataFrame(scores)
    scores['label'] = scores.title.str.contains('active')
    return scores

def processGninaResults(gnina_folder=Config.GNINA_DOCKING_FOLDER):
    for root, dirs, files in os.walk(gnina_folder):
        for file in files:
            if file == "out.sdf.gz":
                try:
                    filepath = os.path.join(root, file)
                    print(filepath)
                    # filepath = f"/home/gomax22/Desktop/Computational-Docking/gnina/docking/1fcq/1-(4-Chlorophenyl)-5-(2-methoxyethoxy)-4-oxo-1,4-dihydrocinnoline-3-carboxylic_acid/out.sdf.gz"
                    scores = processDockingResult(filepath)
                    
                    print(scores)
                except AttributeError:
                    continue
                
                # with open('scores.json', 'w', encoding='utf-8') as f:
                #    json.dump(scores, f, ensure_ascii=False, indent=4)



def compareRMSDs(ref_path, dock_results):
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
    return means


def RMSDComparison(receptor, ligands_folder=Config.LIGANDS_SDF_FOLDER, docking_folders=[Config.VINA_DOCKING_FOLDER, Config.GNINA_DOCKING_FOLDER]):
    
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
                print("WARNING: cannot compute RMSDs for {lig} because docking results don't exist!\n")
                continue
            
            rmsd = compareRMSDs(os.path.join(root, ligand), docking_results)
            print(f"ligand: {lig}\nRMSDs [Vina, GNINA]: {rmsd}\n\n")
            if not checkRMSDCorrectness(rmsd):
                continue
            means_list.append(rmsd)
    
    means_matrix = np.array(means_list, dtype=object)
    results = np.mean(means_matrix, axis=0)
    return [results]