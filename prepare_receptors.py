from MoleculesPreparation.receptorsPreparation import createGridboxes, deleteHeteroatomsChains, prepareReceptors, selectReceptors, splitChains, splitRepeatedResidues
from MoleculesPreparation.structuresManipulation import checkWarnings
from tkinter.messagebox import showinfo
from config import Config
from Utilities.utils import checkFilesInFolder, removeFiles, isWritable
from pathlib import Path
import sys
import getopt
import time


if __name__ == "__main__":

    st = time.time()

    def usage():

        print("Usage: %s" % sys.argv[0])

        print(
            "Optional parameters: \n \
            \t[-v]: verbose output (default is False)\n \
            \t[-E]: define a folder where excel files has to be stored or are stored\n \
            \t[-p]: define a folder where pdbqt files has to be stored or are stored\n \
            \t[-P]: define a folder where pdb files has to be stored or are stored\n \
            \t[-k]: keep pdb files stored into pdb_folder(must be specified after \
            \t[-P] | [--keep-pdb-files])\
            \t[-m]: define margin in angstroms to create protein gridbox for docking (default is 3)\
            \t[-h]: print usage"
        )

    # process command arguments
    try:
        opt_list, args = getopt.getopt(
            sys.argv[1:],
            "E:p:P:m:V:hvk",[]
        )
    except getopt.GetoptError as msg:
        sys.stdout = sys.stderr
        print("prepare_receptors.py: %s" % msg)
        usage()
        sys.exit(2)  # should create our own error handler

    # initialize environment
    print("--------- prepare_receptors.py -----------")
    print("######### INITIALIZE ENVIRONMENT #########")
    print("------------------------------------------")

    # initialize variables
    pdb_folder = Config.RECEPTORS_PDB_FOLDER
    gridbox_output_folder = Config.GRIDBOX_FOLDER
    pdbqt_folder = Config.RECEPTORS_PDBQT_FOLDER
    excel_folder = Config.EXCEL_FOLDER
    url = Config.URL
    verbose = False
    margin = 3
    virtual_box = False
    keep_pdb_files = False
    charges_to_add = 'Kollman'

    for o, a in opt_list:
        
        if o == "-v":
            verbose = True
            print("set verbose to ", verbose)
        
        if o == "-E":
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to excel folder = a
            excel_folder = a
            if verbose:
                print("set excel folder to ", excel_folder)

        if o == "-P":
            # verify path (permissions)
            if not isWritable(a):
                print("ERROR: Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to pdbqt folder = a
            pdbqt_folder = a
            if verbose:
                print("set pdqbt folder to ", pdbqt_folder)

        if o == "-p":
            # verify path (permissions)
            if not isWritable(a):
                print("ERROR: Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to pdb folder = a
            pdb_folder = a
            if verbose:
                print("set pdb folder to ", pdb_folder)

        if o == "-k":
            keep_pdb_files = True
            if verbose:
                print("set keep-pdb-files option to ", True)

        if o == "-m":
            margin = a
            if verbose:
                print("set margin to ", margin)

        if o == "-h":
            usage()
            exit(0)

    # initialize folders
    if pdb_folder == Config.RECEPTORS_PDB_FOLDER:
        Path(Config.RECEPTORS_PDB_FOLDER).mkdir(parents=True, exist_ok=True)
    if pdbqt_folder == Config.RECEPTORS_PDBQT_FOLDER:
        Path(Config.RECEPTORS_PDBQT_FOLDER).mkdir(parents=True, exist_ok=True)
    if gridbox_output_folder == Config.GRIDBOX_FOLDER:
        Path(Config.GRIDBOX_FOLDER).mkdir(parents=True, exist_ok=True)
    if excel_folder == Config.EXCEL_FOLDER:
        Path(Config.EXCEL_FOLDER).mkdir(parents=True, exist_ok=True)

    removeFiles(pdbqt_folder, ".pdbqt")
    removeFiles(gridbox_output_folder, ".txt")

    if keep_pdb_files is False:
        removeFiles(pdb_folder, ".pdb")
        if verbose:
            print("\n------------- RECEPTORS ----------------")
            print("################# STEP 1 #################")
            print("------------------------------------------")
        selectReceptors(
            pdb_folder=pdb_folder,
            excel_folder=excel_folder,
            verbose=verbose
        )
    else:
        # check if there is at least a pdb file
        if not checkFilesInFolder(folder=pdb_folder, docted_extension=".pdb"):
            print("ERROR: There's no pdb file into pdb folder")
            exit(2)
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
    createGridboxes(
        pdb_folder=pdb_folder,
        gridbox_output_folder=gridbox_output_folder,
        margin=margin,
        verbose=verbose,
    )

    if verbose:
        print("\n---------- RECEPTORS: COMPLETED ---------")

    et = time.time()

    elapsed_time = et - st 

    showinfo("Process completed", "Receptors preparation has been completed successfully in {:.2f} seconds".format(elapsed_time))