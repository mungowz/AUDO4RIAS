import os
from config import Config
from ligands.extract_3D_structures import extract_3d_structures
from ligands.sdf_to_pdb import sdf_to_pdb
from ligands.pdb_to_pdbqt import pdb_to_pdbqt
from pathlib import Path
from utils import isWritable

if __name__ == "__main__":
    import sys
    import getopt

    def usage():
        print("Usage: %s" % sys.argv[0])

        print(
            "Optional parameters: \n \
            \t[-v] | [--verbose]: verbose output (default is False)\n \
            \t[-e] | [--excel-file]: define an excel file as input file to select needed ligands\n \
            \t[-E] | [--excel-folder]: define a folder where excel files has to be stored or are stored\n \
            \t[-s] | [--sdf-folder]: define a folder where sdf files has to be stored or are stored\n \
            \t[-p] | [--pdbqt-folder]: define a folder where pdbqt files has to be stored or are stored\n \
            \t[-P] | [--pdb-folder]: define a folder where pdb files has to be stored or are stored\n \
            \t[-k] | [--keep-ligands]: keep ligands stored into sdf folder (default is False)\n \
            \t[-h] | [--help]: print usage" 
        )

    # process command arguments
    try:
        opt_list, args = getopt.getopt(
            sys.argv[1:],
            "e:E:s:P:p:khv",
            [
                "excel-file",
                "excel-folder",
                "sdf-folder",
                "pdbqt-folder",
                "pdb-folder",
                "keep-ligands",
                "help",
                "verbose",
            ],
        )
    except getopt.GetoptError as msg:
        sys.stdout = sys.stderr
        print("prepare_ligands.py: %s" % msg)
        usage()
        sys.exit(2)  # should create our own error handler

    # initialize environment
    print("----------- prepare_ligands.py -----------")
    print("######### INITIALIZE ENVIRONMENT #########")
    print("------------------------------------------")

    # initialize variables
    excel_folder = Config.EXCEL_FOLDER
    excel_file = os.path.join(excel_folder, "pest_group_MOA.xlsx")
    sdf_folder = Config.LIGANDS_SDF_FOLDER
    pdbqt_folder = Config.LIGANDS_PDBQT_FOLDER
    pdb_folder = Config.LIGANDS_PDB_FOLDER
    keep_ligands = False
    verbose = False

    for o, a in opt_list:
        if o in ("-v", "--verbose"):
            # set verbose to true
            verbose = True
            print("set verbose to ", verbose)

        if o in ("-e", "--excel-file"):
            # verify path ? (existance, permissions)
            # set path to excel file = a
            excel_file = a
            if verbose:
                print("set excel filepath to ", excel_file)

        if o in ("-E", "--excel-folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to excel folder = a
            excel_folder = a
            if verbose:
                print("set excel folder to ", excel_folder)

        if o in ("-s", "--sdf-folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to sdf folder = a
            sdf_folder = a
            if verbose:
                print("set sdf folder to ", sdf_folder)

        if o in ("-P", "--pdbqt-folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to pdbqt folder = a
            pdbqt_folder = a
            if verbose:
                print("set pdqbt folder to ", pdbqt_folder)

        if o in ("-p", "--pdb-folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to pdb folder = a
            pdb_folder = a
            if verbose:
                print("set pdb folder to ", pdb_folder)

        if o in ("-k", "--keep-ligands"):
            # check if -s or default sdf folder contains sdf files (?)
            # keep ligands stored into sdf folder
            keep_ligands = True
            if verbose:
                print("set keep-ligands option to ", keep_ligands)

        if o in ("-h", "--help"):
            usage()
            exit(0)

    # initialize folders
    if sdf_folder == Config.LIGANDS_SDF_FOLDER:
        Path(Config.LIGANDS_SDF_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdb_folder == Config.LIGANDS_PDB_FOLDER:
        Path(Config.LIGANDS_PDB_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdbqt_folder == Config.LIGANDS_PDBQT_FOLDER:
        Path(Config.LIGANDS_PDBQT_FOLDER).mkdir(parents=True, exist_ok=True)
    if excel_folder == Config.EXCEL_FOLDER:
        Path(Config.EXCEL_FOLDER).mkdir(parents=True, exist_ok=True)

    ## cannot specify keep ligands and excel_file ##
    #if not keep_ligands:
    if verbose:
        print("---------------- LIGANDS -----------------")
        print("################# STEP 1 #################")
        print("------------------------------------------")
    
    extract_3d_structures(
        excel_path=excel_file,
        sdf_folder=sdf_folder,
        excel_folder=excel_folder,
        keep_ligands=keep_ligands,
        verbose=verbose
    )
    
    if verbose:
        print("---------------- LIGANDS -----------------")
        print("################# STEP 2 #################")
        print("------------------------------------------")
    
    sdf_to_pdb(
            sdf_folder=sdf_folder, 
            pdb_folder=pdb_folder, 
            verbose=verbose,
        )
    
    if verbose:
        print("---------------- LIGANDS -----------------")
        print("################# STEP 3 #################")
        print("------------------------------------------")
    
    pdb_to_pdbqt(
        pdb_folder=pdb_folder,
        pdbqt_folder=pdbqt_folder,
        verbose=verbose
    )

    if verbose:
        print("----------- LIGANDS: COMPLETED -----------")
