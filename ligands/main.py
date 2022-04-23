import sys
import getopt
from ligands.extract_3D_structures import extract_3d_structures
from ligands.sdf_to_pdbqt import sdf_to_pdbqt
from ligands.exec_prepare_ligands import exec_prepare_ligands
from ligands.prepare_ligands import prepare_ligands

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvutl", ["help=", "verbose="])
    except getopt.error as msg: 
        sys.stdout = sys.stderr
        print(msg)
        print("""usage: %s [-h, --help|-v, --verbose|-u |-t |-l ]
        -h, --help: help
        -v, --verbose: verbose
        -u: extract_3d_structures
        -t: sdf_to_pdbqt
        -l: prepare_ligands (default)"""%sys.argv[0])
        sys.exit(2)

    for o, a in opts: 
        if o == "-u": extract_3d_structures()
        elif o == "-t": sdf_to_pdbqt()
        elif o == "-l": prepare_ligands()
        else: prepare_ligands()