from Gui.scripts.receptorsPreparation2 import selectReceptors, splitRepeatedResidues, deleteHeteroatomsChains, splitChains, prepareReceptors, createGridboxes, checkWarnings
from config import Config
from Utilities.utils import checkFilesInFolder, removeFiles
from pathlib import Path
from tkinter.messagebox import showerror
from os.path import exists


def prepare_receptors(verbose, excel_folder, pdb_folder, pdbqt_folder, margin, keep_pdb_files, gridbox_output_folder, charges_to_add):
    
    print("set excel folder to ", excel_folder)
    print("set pdb folder to ", pdb_folder)
    print("set pdbqt folder to ", pdbqt_folder)
    print("set gridbox folder to ", gridbox_output_folder)
    print("set keep-pdb-files option to ", bool(keep_pdb_files))
    print("set margin to ", margin)

    print("--------- prepare_receptors.py -----------")
    print("######### INITIALIZE ENVIRONMENT #########")
    print("------------------------------------------")

    # initialize folders
    if pdb_folder == Config.RECEPTORS_PDB_FOLDER:
        Path(Config.RECEPTORS_PDB_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdbqt_folder == Config.RECEPTORS_PDBQT_FOLDER:
        Path(Config.RECEPTORS_PDBQT_FOLDER).mkdir(parents=True, exist_ok=True)
    if gridbox_output_folder == Config.GRIDBOX_FOLDER:
        Path(Config.GRIDBOX_FOLDER).mkdir(parents=True, exist_ok=True)

    removeFiles(pdbqt_folder, ".pdbqt")
    removeFiles(gridbox_output_folder, ".txt")

    if not keep_pdb_files:
        removeFiles(pdb_folder, ".pdb")
        if verbose:
            print("\n------------- RECEPTORS ----------------")
            print("################# STEP 1 #################")
            print("------------------------------------------")
        selectReceptors(pdb_folder=pdb_folder, excel_folder=excel_folder, verbose=verbose)
    else:
        # check if there is at least a pdb file
        if not checkFilesInFolder(folder=pdb_folder, docted_extension=".pdb"):
            showerror("Error", "There's no pdb file into pdb folder")
            return
        if verbose:
            print("\n--------------- RECEPTORS ----------------")
            print("############# SKIPPED STEP 1.1 #############")
            print("--------------------------------------------")

    if verbose:
        checkWarnings(pdb_folder=pdb_folder)
        print("\n------------- RECEPTORS ----------------")
        print("################# STEP 2 #################")
        print("------------------------------------------")

    splitRepeatedResidues(pdb_folder=pdb_folder, verbose=verbose)
    deleteHeteroatomsChains(pdb_folder=pdb_folder, verbose=verbose)
    splitChains(pdb_folder=pdb_folder, verbose=verbose)

    prepareReceptors(pdb_folder=pdb_folder, pdbqt_folder=pdbqt_folder, verbose=verbose, charges_to_add=charges_to_add)

    if verbose:
        print("\n------------- RECEPTORS ----------------")
        print("################# STEP 3 #################")
        print("------------------------------------------")
    createGridboxes(pdb_folder=pdb_folder, gridbox_output_folder=gridbox_output_folder, margin=margin, verbose=verbose)

    if verbose:
        print("\n---------- RECEPTORS: COMPLETED ---------")
