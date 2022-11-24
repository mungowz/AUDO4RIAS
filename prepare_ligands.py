import os
from MoleculesPreparation.ligandsPreparation import prepareLigands, selectLigands
from Utilities.utils import checkFilesInFolder, removeFiles
from config import Config
from pathlib import Path
from Utilities.utils import isWritable
from MoleculesPreparation.structuresManipulation import sdf2pdb

if __name__ == "__main__":
    import sys
    import getopt

    def usage():
        print("Usage: %s" % sys.argv[0])

        print(
            "Optional parameters: \n \
            \t[-v]: verbose output (default is False)\n \
            \t[-e]: define an excel file as input file to select needed ligands\n \
            \t[-E]: define a folder where excel files has to be stored or are stored\n \
            \t[-s]: define a folder where sdf files has to be stored or are stored\n \
            \t[-p]: define a folder where pdbqt files has to be stored or are stored\n \
            \t[-P]: define a folder where pdb files has to be stored or are stored\n \
            \t[-k]: keep ligands stored into sdf folder (default is False)\n \
            \t[-h]: print usage" 
        )

    # process command arguments
    try:
        opt_list, args = getopt.getopt(
            sys.argv[1:],
            "i:e:s:P:p:khv",
            []
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
    default_file = os.path.join(Config.INPUT_FOLDER, "ligands_list.txt")
    input_file = default_file
    sdf_folder = Config.LIGANDS_SDF_FOLDER
    pdbqt_folder = Config.LIGANDS_PDBQT_FOLDER
    pdb_folder = Config.LIGANDS_PDB_FOLDER
    keep_ligands = False
    verbose = False

    for o, a in opt_list:
        if o == "-v":
            # set verbose to true
            verbose = True
            print("set verbose to ", verbose)

        if o == "-i":
            # verify path  (existance, permissions)
            # set path to input file = a
            if not os.path.exists(a):
                print("Specify a valid input file!")
                exit(1)
            if not os.access(a, os.R_OK):
                print("Modify file permission!")
                exit(1)
            input_file = a
            if verbose:
                print("set input filepath to ", input_file)

        if o == "-e":
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to excel folder = a
            excel_folder = a
            if verbose:
                print("set excel folder to ", excel_folder)

        if o == "-s":
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to sdf folder = a
            sdf_folder = a
            if verbose:
                print("set sdf folder to ", sdf_folder)

        if o == "-P":
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to pdbqt folder = a
            pdbqt_folder = a
            if verbose:
                print("set pdqbt folder to ", pdbqt_folder)

        if o == "-p":
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to pdb folder = a
            pdb_folder = a
            if verbose:
                print("set pdb folder to ", pdb_folder)

        if o == "-k":
            # check if -s or default sdf folder contains sdf files (?)
            # keep ligands stored into sdf folder
            keep_ligands = True
            if verbose:
                print("set keep-ligands option to ", keep_ligands)

        if o == "-h":
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


    if keep_ligands is True and input_file != default_file:
        print("You cannot specify either --keep_ligands and --input_file!")
        exit(1)
    

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
