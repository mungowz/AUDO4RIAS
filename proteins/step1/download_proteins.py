from biopandas.pdb import PandasPdb
import os


def download_proteins(proteins_list, protein_folder):

    # PandasPdb object
    ppdb = PandasPdb()

    # download only pdb files that aren't already downloaded
    for protein_code in proteins_list:
        protein_file = protein_code + ".pdb"
        for root, dirs, files in os.walk(protein_folder):
            if protein_file not in files:

                # Initialize a new PandasPdb object
                # and fetch the PDB file from rcsb.org
                ppdb.fetch_pdb(protein_code)

                # save dataframe as pdb file
                output_file = protein_folder + "\{protein_code}.pdb".format(
                    protein_code=protein_code
                )
                ppdb.to_pdb(output_file)
            else:
                print(protein_code + ": OK")

            # print(ppdb.df)
