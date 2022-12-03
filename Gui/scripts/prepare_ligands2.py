from Gui.scripts.ligandsPreparation2 import selectLigands, sdf2pdb, prepareLigands
from Utilities.utils import removeFiles, checkFilesInFolder
from config import Config
from tkinter.messagebox import showerror
from pathlib import Path


def prepare_ligands(verbose, input_file, excel_folder, sdf_folder, pdb_folder, pdbqt_folder, keep_ligands, contents):

    print("set input filepath to ", input_file)
    print("set excel folder to ", excel_folder)
    print("set sdf folder to ", sdf_folder)
    print("set pdbqt folder to ", pdbqt_folder)
    print("set keep-ligands option to ", bool(keep_ligands))
    print("set pdbqt folder to ", pdbqt_folder)
    print("set keep-ligands option to ", bool(keep_ligands))

    print("------------------------------------------")
    print("######### INITIALIZE ENVIRONMENT #########")
    print("------------------------------------------")

    # initialize folders
    if sdf_folder == Config.LIGANDS_SDF_FOLDER:
        Path(Config.LIGANDS_SDF_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdb_folder == Config.LIGANDS_PDB_FOLDER:
        Path(Config.LIGANDS_PDB_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdbqt_folder == Config.LIGANDS_PDBQT_FOLDER:
        Path(Config.LIGANDS_PDBQT_FOLDER).mkdir(parents=True, exist_ok=True)
    if excel_folder == Config.EXCEL_FOLDER:
        Path(Config.EXCEL_FOLDER).mkdir(parents=True, exist_ok=True)

    if not keep_ligands:
        removeFiles(sdf_folder, ".sdf")
        if verbose:
            print("---------------- LIGANDS -----------------")
            print("################# STEP 1 #################")
            print("------------------------------------------")

        selectLigands(sdf_folder, excel_folder, verbose, contents)

    else: 
        # check if there is at least a sdf file
        if not checkFilesInFolder(folder=sdf_folder, docted_extension=".sdf"):
            showerror("Error", "There's no sdf file into sdf folder")
            return
        if verbose:
            print("\n--------------- LIGANDS ------------------")
            print("############# SKIPPED STEP 1.1 #############")
            print("--------------------------------------------")
    
    if verbose:
        print("---------------- LIGANDS -----------------")
        print("################# STEP 2 #################")
        print("------------------------------------------")
            

    sdf2pdb(sdf_folder, pdb_folder, verbose)
    
    if verbose:
        print("---------------- LIGANDS -----------------")
        print("################# STEP 3 #################")
        print("------------------------------------------")
    
    prepareLigands(pdb_folder, pdbqt_folder, verbose)

    if verbose:
        print("----------- LIGANDS: COMPLETED -----------")