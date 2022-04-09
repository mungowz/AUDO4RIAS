from biopandas.pdb import PandasPdb
import os


def download_pdbs(pdbs_list=[], output_path=None):

    # PandasPdb object
    ppdb = PandasPdb()

    # download only pdb files that aren't already downloaded
    for protein_code in pdbs_list:

        #   print("Downloading pdb file for {code}...".format(code=protein_code))
        protein_file = protein_code + ".pdb"

        for root, dirs, files in os.walk(output_path):
            output_file = output_path + "\{protein_code}.pdb".format(
                protein_code=protein_code
            )
            if protein_file not in files:

                # Initialize a new PandasPdb object
                # and fetch the PDB file from rcsb.org
                ppdb.fetch_pdb(protein_code)

                # save dataframe as pdb file
                ppdb.to_pdb(output_file)

                print(
                    "{protein_code}.pdb downloaded! (Stored in {output_file})".format(
                        protein_code=protein_code, output_file=output_file
                    )
                )
            else:
                print(
                    "Already downloaded pdb file for {code}! Stored in {output_file}".format(
                        code=protein_code, output_file=output_file
                    )
                )

            # print(ppdb.df)
