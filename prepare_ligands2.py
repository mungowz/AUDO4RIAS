import os
from MoleculesPreparation.ligandsPreparation import prepareLigands, selectLigands
from Utilities.utils import checkFilesInFolder, removeFiles
from config import Config
from pathlib import Path
from Utilities.utils import isWritable
from MoleculesPreparation.structuresManipulation import sdf2pdb

def prepare_ligands(
    verbose, 
    excel_file, 
    input_file, 
    excel_folder_flag, 
    excel_folder, 
    sdf_folder_flag, 
    sdf_folder, 
    pdb_folder_flag, 
    pdb_folder, 
    pdbqt_folder_flag,
    pdbqt_folder,
    keep_ligands
):
        
    print("------------------------------------------")
    print("######### INITIALIZE ENVIRONMENT #########")
    print("------------------------------------------")

    if excel_file is not None:
        if not os.path.exists(excel_file):
            print("Specify a valid excel file!")
            exit(1)
        if os.access(excel_file, os.R_OK):
            print("Modify file permission!")
            exit(1)
        input_file = excel_file
        print("set input filepath to ", input_file)

        if excel_folder_flag:
            if not isWritable(excel_folder):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            print("set excel folder to ", excel_folder)

        if sdf_folder_flag:
            if not isWritable(sdf_folder):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            print("set sdf folder to ", sdf_folder)

        if pdb_folder_flag:
            if not isWritable(pdb_folder):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            print("set pdb folder to ", pdb_folder)

        if pdbqt_folder_flag:
            if not isWritable(pdbqt_folder):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            print("set pdbqt folder to ", pdbqt_folder)

        print("set keep-ligands option to ", keep_ligands)


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
    
        selectLigands(
            input_path=input_file,
            sdf_folder=sdf_folder,
            excel_folder=excel_folder,
            verbose=verbose
        )
    else: 
        # check if there is at least a sdf file
        if not checkFilesInFolder(folder=sdf_folder, docted_extension=".sdf"):
            print("ERROR: There's no sdf file into sdf folder")
            exit(2)
        if verbose:
            print("\n--------------- LIGANDS ------------------")
            print("############# SKIPPED STEP 1.1 #############")
            print("--------------------------------------------")
    
    if verbose:
        print("---------------- LIGANDS -----------------")
        print("################# STEP 2 #################")
        print("------------------------------------------")
            

    sdf2pdb(
        sdf_folder=sdf_folder, 
        pdb_folder=pdb_folder, 
        verbose=verbose,
    )
    
    if verbose:
        print("---------------- LIGANDS -----------------")
        print("################# STEP 3 #################")
        print("------------------------------------------")
    
    prepareLigands(
        pdb_folder=pdb_folder,
        pdbqt_folder=pdbqt_folder,
        verbose=verbose
    )

    if verbose:
        print("----------- LIGANDS: COMPLETED -----------")
