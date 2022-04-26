from config import Config
from proteins.PDB_info_extraction import pdb_info_extraction
from proteins.create_gridbox import create_gridbox
from proteins.exec_prepare_receptors import prepare_receptors
from proteins.split_chains import split_chains
from proteins.split_repeated_residues import split_repeated_residues


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
            \t[-q] | [--query-type]: define the query for proteins selection in ['DEFAULT', 'ALTERNATIVE'] (default is DEFAULT)\
            \t[-l] | [--maximum-length]: define maximum sequence length for proteins selection (default is 40)\
            \t[-i] | [--include-mutants]: include mutants for proteins selection (default is False)\
            \t[-m] | [--margin]: define margin in angstroms to create protein gridbox for dockinf (default is 3)\
            \t[-h] | [--help]: print usage"
        )

    # process command arguments
    try:
        opt_list, args = getopt.getopt(
            sys.argv[1:],
            "E:p:P:im:q:l:hv",
            [
                "excel-folder",
                "pdbqt-folder",
                "pdb-folder",
                "include-mutants",
                "margin",
                "query-type",
                "maximum_length",
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
    query_type = Config.QUERY_TYPE
    gridbox_output_folder = Config.GRIDBOX_OUTPUT_FOLDER
    pdbqt_folder = Config.PDBQT_PROTEINS_FOLDER
    excel_folder = Config.EXCEL_FOLDER
    verbose = False
    margin = 3
    include_mutants = False
    maximum_length = 40

    for o, a in opt_list:
        if o in ("-v", "--verbose"):
            verbose = True
            print("set verbose to ", verbose)
        if o in ("-E", "--excel-folder"):
            # verify path ? (permissions)
            # set path to sdf folder = a
            excel_folder = a
            if verbose:
                print("set excel folder to ", excel_folder)
        if o in ("-P", "--pdbqt-folder"):
            # verify path ? (permissions)
            # set path to pdbqt folder = a
            pdbqt_folder = a
            if verbose:
                print("set pdqbt folder to ", pdbqt_folder)

        if o in ("-p", "--pdb-folder"):
            # verify path ? (permissions)
            # set path to pdb folder = a
            pdb_folder = a
            if verbose:
                print("set pdb folder to ", pdb_folder)
        if o in ("-i", "--include-mutants"):
            # include mutants in proteins selection
            include_mutants = a
            if verbose:
                print("set include-mutants option to ", include_mutants)

        if o in ("-m", "--margin"):
            margin = a
            if verbose:
                print("set margin to ", margin)

        if o in ("-q", "--query-type"):
            query_type = a
            if verbose:
                print("set query-type to ", query_type)

        if o in ("-l", "--maximum-length"):
            maximum_length = a
            if verbose:
                print("set maximum sequence to ", maximum_length)

        if o in ("-h", "--help"):
            usage()
            exit(0)
    if verbose:
        print("---------------- PROTEINS ----------------")
        print("################# STEP 1 #################")
        print("------------------------------------------")
    pdb_info_extraction(
        query_type=query_type,
        maximum_length=maximum_length,
        include_mutants=include_mutants,
        pdb_folder=pdb_folder,
        excel_folder=excel_folder,
        verbose=verbose,
    )

    if verbose:
        print("---------------- PROTEINS ----------------")
        print("################# STEP 2 #################")
        print("------------------------------------------")

    split_repeated_residues(pdb_folder=pdb_folder, verbose=verbose)
    split_chains(pdb_folder=pdb_folder, verbose=verbose)
    prepare_receptors(pdb_folder=pdb_folder, pdbqt_folder=pdbqt_folder, verbose=verbose)

    if verbose:
        print("---------------- PROTEINS ----------------")
        print("################# STEP 3 #################")
        print("------------------------------------------")
    create_gridbox(
        pdb_folder=pdb_folder,
        gridbox_output_folder=gridbox_output_folder,
        margin=margin,
        verbose=verbose,
    )

    if verbose:
        print("----------- PROTEINS: COMPLETED ----------")
