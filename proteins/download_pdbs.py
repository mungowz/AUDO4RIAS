import os
from prody import confProDy, fetchPDB


def download_pdbs(pdbs_list, output_path, verbose):
    if not verbose:
        confProDy(verbosity="none")

    # download only pdb files that aren't already downloaded
    for protein_code in pdbs_list:
        for root, dirs, files in os.walk(output_path):
            output_file = os.path.join(output_path, protein_code + ".pdb")

            # fetch the PDB file from rcsb.org
            fetchPDB(protein_code, folder=output_path, compressed=False)
            print("\n")
