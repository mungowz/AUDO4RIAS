from biopandas.pdb import PandasPdb
import os


def download_pdbs(pdbs_list=[], output_path=None):

    # PandasPdb object
    ppdb = PandasPdb()

    # download only pdb files that aren't already downloaded
    for protein_code in pdbs_list:
        protein_file = protein_code + ".pdb"
        for root, dirs, files in os.walk(output_path):
            if protein_file not in files:

                # Initialize a new PandasPdb object
                # and fetch the PDB file from rcsb.org
                ppdb.fetch_pdb(protein_code)

                # save dataframe as pdb file
                output_file = output_path + "\{protein_code}.pdb".format(
                    protein_code=protein_code
                )
                ppdb.to_pdb(output_file)
            else:
                print(protein_code + ": OK")

            # print(ppdb.df)
