from config import Config
from proteins.PDB_info_extraction import pdb_info_extraction
from proteins.create_gridbox import create_gridbox
from proteins.exec_prepare_receptors import prepare_receptors
from proteins.split_chains import split_chains
from proteins.split_repeated_residues import split_repeated_residues
from proteins.extract_remarks import check_warnings
from proteins.clear_hetatm import clear_hetatm
from utils import check_files_in_folder, remove_files, isWritable
from web_view import web_view
from pathlib import Path

if __name__ == "__main__":
    import sys
    import getopt

    def usage():
        print("Usage: %s" % sys.argv[0])

        print(
            "Optional parameters: \n \
            \t[-v] | [--verbose]: verbose output (default is False)\n \
            \t[-E] | [--excel-folder]: define a folder where excel files has to be stored or are stored\n \
            \t[-p] | [--pdbqt-folder]: define a folder where pdbqt files has to be stored or are stored\n \
            \t[-P] | [--pdb-folder]: define a folder where pdb files has to be stored or are stored\n \
            \t[-k] | [--keep-pdb-files]: keep pdb files stored into pdb_folder(must be specified after [-P] | [--keep-pdb-files])\
            \t[-m] | [--margin]: define margin in angstroms to create protein gridbox for docking (default is 3)\
            \t[-h] | [--help]: print usage"
        )

    # process command arguments
    try:
        opt_list, args = getopt.getopt(
            sys.argv[1:],
            "E:p:P:m:hvk",
            [
                "excel-folder",
                "pdbqt-folder",
                "pdb-folder",
                "margin",
                "keep-pdb-files",
                "help",
                "verbose",
            ],
        )
    except getopt.GetoptError as msg:
        sys.stdout = sys.stderr
        print("prepare_receptors.py: %s" % msg)
        usage()
        sys.exit(2)  # should create our own error handler

    # initialize environment
    print("----------- prepare_receptors.py -----------")
    print("######### INITIALIZE ENVIRONMENT #########")
    print("------------------------------------------")

    # initialize variables
    pdb_folder = Config.PROTEINS_FOLDER
    gridbox_output_folder = Config.GRIDBOX_OUTPUT_FOLDER
    pdbqt_folder = Config.PDBQT_PROTEINS_FOLDER
    excel_folder = Config.EXCEL_FOLDER
    url = Config.URL
    verbose = False
    margin = 3
    keep_pdb_files = False
    charges_to_add = 'Kollman'

    for o, a in opt_list:
        if o in ("-v", "--verbose"):
            verbose = True
            print("set verbose to ", verbose)
        if o in ("-E", "--excel-folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to excel folder = a
            excel_folder = a
            if verbose:
                print("set excel folder to ", excel_folder)
        if o in ("-P", "--pdbqt-folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("ERROR: Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to pdbqt folder = a
            pdbqt_folder = a
            if verbose:
                print("set pdqbt folder to ", pdbqt_folder)

        if o in ("-p", "--pdb-folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("ERROR: Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to pdb folder = a
            pdb_folder = a
            if verbose:
                print("set pdb folder to ", pdb_folder)

        if o in ("-k", "--keep-pdb-files"):
            # check if there is at least a pdb file
            keep_pdb_files = True
            if verbose:
                print("set keep-pdb-files option to ", True)

        if o in ("-m", "--margin"):
            margin = a
            if verbose:
                print("set margin to ", margin)

        if o in ("-h", "--help"):
            usage()
            exit(0)

    # initialize folders
    if pdb_folder == Config.PROTEINS_FOLDER:
        Path(Config.PROTEINS_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdbqt_folder == Config.PDBQT_PROTEINS_FOLDER:
        Path(Config.PDBQT_PROTEINS_FOLDER).mkdir(parents=True, exist_ok=True)
    if gridbox_output_folder == Config.GRIDBOX_OUTPUT_FOLDER:
        Path(Config.GRIDBOX_OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

    remove_files(pdbqt_folder, ".pdbqt")
    remove_files(gridbox_output_folder, ".txt")

    if keep_pdb_files is False:
        remove_files(pdb_folder, ".pdb")
        if verbose:
            print("\n---------------- PROTEINS ----------------")
            print("################# STEP 1 #################")
            print("------------------------------------------")
        pdb_info_extraction(
            pdb_folder=pdb_folder,
            excel_folder=excel_folder,
            verbose=verbose,
        )
    else:
        if not check_files_in_folder(folder=pdb_folder, docted_extension=".pdb"):
            print("ERROR: There's no pdb file into pdb folder")
            exit(2)
        if verbose:
            print("\n---------------- PROTEINS ----------------")
            print("############# SKIPPED STEP 1.1 #############")
            print("------------------------------------------")

    if verbose:
        check_warnings(pdb_folder=pdb_folder)
        print("\n---------------- PROTEINS ----------------")
        print("################# STEP 2 #################")
        print("------------------------------------------")

    split_repeated_residues(pdb_folder=pdb_folder, verbose=verbose)
    clear_hetatm(pdb_folder=pdb_folder, verbose=verbose)
    split_chains(pdb_folder=pdb_folder, verbose=verbose)

    prepare_receptors(pdb_folder=pdb_folder, pdbqt_folder=pdbqt_folder, verbose=verbose, charges_to_add=charges_to_add)

    if verbose:
        print("\n---------------- PROTEINS ----------------")
        print("################# STEP 3 #################")
        print("------------------------------------------")
    create_gridbox(
        pdb_folder=pdb_folder,
        gridbox_output_folder=gridbox_output_folder,
        margin=margin,
        verbose=verbose,
    )

    if verbose:
        print("\n----------- PROTEINS: COMPLETED ----------")
