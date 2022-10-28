from MoleculesPreparation.structuresManipulation import checkWarnings
from Gui.receptorsPreparation2 import selectReceptors, createGridboxes, deleteHeteroatomsChains, prepareReceptors, splitChains, splitRepeatedResidues
from Gui.progressBar import ProgressBar
from config import Config
from Utilities.utils import checkFilesInFolder, removeFiles, isWritable
from pathlib import Path
from tkinter import messagebox
import os


def prepare_receptors(
                        verbose,  
                        excel_folder, 
                        pdb_folder, 
                        pdbqt_folder,
                        margin,
                        keep_pdb_files,
                        gridbox_output_folder,
                        charges_to_add
):
    
    # initialize environment
    print("--------- prepare_receptors.py -----------")
    print("######### INITIALIZE ENVIRONMENT #########")
    print("------------------------------------------")
    
    if excel_folder != Config.EXCEL_FOLDER:
        if not os.path.exists(excel_folder):
            messagebox.showerror("Error", "Specify a valid directory or modify dir permission for excel folder!")
            exit(1)
        print("set excel folder to ", excel_folder)
    
    if pdb_folder != Config.LIGANDS_PDB_FOLDER:
        if not os.path.exists(pdb_folder):
            messagebox.showerror("Error", "Specify a valid directory or modify dir permission for pdb folder!")
            exit(1)
        print("set pdb folder to ", pdb_folder)

    if pdbqt_folder != Config.LIGANDS_PDBQT_FOLDER:
        if not os.path.exists(pdbqt_folder):
            messagebox.showerror("Error", "Specify a valid directory or modify dir permission for pdbqt folder!")
            exit(1)
        print("set pdbqt folder to ", pdbqt_folder)

    print("set keep-pdb-files option to ", keep_pdb_files)

    print("set margin to ", margin)

    # initialize folders
    if pdb_folder == Config.RECEPTORS_PDB_FOLDER:
        Path(Config.RECEPTORS_PDB_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdbqt_folder == Config.RECEPTORS_PDBQT_FOLDER:
        Path(Config.RECEPTORS_PDBQT_FOLDER).mkdir(parents=True, exist_ok=True)
    if gridbox_output_folder == Config.GRIDBOX_FOLDER:
        Path(Config.GRIDBOX_FOLDER).mkdir(parents=True, exist_ok=True)

    removeFiles(pdbqt_folder, ".pdbqt")
    removeFiles(gridbox_output_folder, ".txt")

    pb = ProgressBar("Downloading proteins", 100, False)
    pb.update()
    if keep_pdb_files is False:
        removeFiles(pdb_folder, ".pdb")
        if verbose:
            print("\n------------- RECEPTORS ----------------")
            print("################# STEP 1 #################")
            print("------------------------------------------")
        selectReceptors(
            pdb_folder=pdb_folder,
            excel_folder=excel_folder,
            verbose=verbose,
            pb=pb
        )
    else:
        # check if there is at least a pdb file
        if not checkFilesInFolder(folder=pdb_folder, docted_extension=".pdb"):
            messagebox("Error", "There's no pdb file into pdb folder")
            exit(2)
        if verbose:
            print("\n--------------- RECEPTORS ----------------")
            print("############# SKIPPED STEP 1.1 #############")
            print("--------------------------------------------")

    pb.progress()
    pb.update()

    if verbose:
        checkWarnings(pdb_folder=pdb_folder)
        print("\n------------- RECEPTORS ----------------")
        print("################# STEP 2 #################")
        print("------------------------------------------")

    splitRepeatedResidues(pdb_folder=pdb_folder, verbose=verbose, pb=pb)
    deleteHeteroatomsChains(pdb_folder=pdb_folder, verbose=verbose, pb=pb)
    splitChains(pdb_folder=pdb_folder, verbose=verbose, pb=pb)

    prepareReceptors(pdb_folder=pdb_folder, pdbqt_folder=pdbqt_folder, verbose=verbose, charges_to_add=charges_to_add, pb=pb)

    if verbose:
        print("\n------------- RECEPTORS ----------------")
        print("################# STEP 3 #################")
        print("------------------------------------------")
    createGridboxes(
        pdb_folder=pdb_folder,
        gridbox_output_folder=gridbox_output_folder,
        margin=margin,
        verbose=verbose,
        pb=pb
    )

    pb.close()

    if verbose:
        print("\n---------- RECEPTORS: COMPLETED ---------")
