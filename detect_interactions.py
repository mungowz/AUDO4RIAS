#! /bin/python
from config import Config
import os



# This script relies on MGLTools packages, written in Python2
# Because of compatibility problems between Python versions (2 and 2.5+), this script cannot be executed without errors by Python binaries but
# a good solution is given by using .../MGLTools-1.5.6/bin/pythonsh
if __name__ == "__main__":
    import sys
    import getopt
    from InteractionsAnalysis.interactionsDetection import detectInteractions

    def usage():
        print("Analyze docking results to detect interactions of protein-ligand complexes.\
            It could takes a long time depending from the amount of protein-ligand complexes.\
        Usage: %s [-s] <software>" % sys.argv[0])

        print(
            "Optional parameters: \n \
            \t[-s] | [--software]: set a specific software whose analyze results in [Vina, GNINA] (default is Vina)\n \
            \t[-h] | [--help]: print usage"
        )

    # process command arguments
    try:
        opt_list, args = getopt.getopt(
            sys.argv[1:],
            "hs:",
            [
                "--help",
                "--software"
            ],
        )
    except getopt.GetoptError:
        sys.stdout = sys.stderr
        print("detect_interactions.py: %s" % getopt.GetoptError.msg)
        usage()
        sys.exit(2)  # should create our own error handler

    # initialize environment
    macro_folder = Config.RECEPTORS_PDBQT_FOLDER
    docking_folder = Config.VINA_DOCKING_FOLDER
    docking_softwares = ["vina", "gnina"]
    for o, a in opt_list:
        if o in ("-s", "--software"):
            if a.lower() not in docking_softwares:
                print("Invalid software specified")
                exit(1)
            
            if a.lower() == "gnina":
                docking_folder = Config.GNINA_DOCKING_FOLDER

        if o in ("-h", "--help"):
            usage()
            exit(0)

    detectInteractions(macro_folder, docking_folder)


