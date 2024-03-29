from InteractionsAnalysis.resultsProcessing import RMSDComparison
from Utilities.utils import isWritable
from config import Config


if __name__ == "__main__":
    import sys
    import getopt
    def usage():
        print(
        "Compares docking results in terms of Symmetric-Corrected RMSD\n\
Usage: %s -r <receptor> [-L <folder>] [-h]\n" % sys.argv[0])

        print(
            "Description of parameters: \n\
\t-r              Select the receptor involved in protein-ligand docked complex\n\
Optional parameters: \n\
\t-L        set the folder where are stored ligands in .sdf format\n\
\t-h        print usage\n"
        )

    # process command arguments
    try:
        opt_list, args = getopt.getopt(
            sys.argv[1:],
            "hr:L:", []
        )
    except getopt.GetoptError:
        sys.stdout = sys.stderr
        print("RMSDComparison.py: %s" % getopt.GetoptError.msg)
        usage()
        sys.exit(2)  # should create our own error handler

    # initialize environment
    ligands_folder = Config.LIGANDS_SDF_FOLDER
    docking_folders = [Config.VINA_DOCKING_FOLDER, Config.GNINA_DOCKING_FOLDER]
    receptor = None


    for o, a in opt_list:
        if o == "-r":
            print(f"set receptor to {a}")
            receptor = a
        if o == "-L":
            if not isWritable(a):
                print("Invalid ligands folder: does not exists or no read permissions!")
                exit(1)
            ref_path = a
        if o == "-h":
            usage()
            exit(0)
    if receptor is None:
        print("You must specify a receptor code!")
        usage()
        exit(1)

    results = RMSDComparison(receptor, ligands_folder, docking_folders)
    magnitude = "{:.1e}".format(abs(results[0][0] - results[0][1]))

    print(f"VINA: {results[0][0]}\nGNINA:{results[0][1]}\nMAGNITUDE:{magnitude}")