from biopandas.pdb import PandasPdb
import os
import pandas as pd
import openpyxl
from config import Config


def split_repeated_residues(
    input_folder=Config.PROTEINS_FOLDER, output_folder=Config.PROTEINS_FOLDER
):
    ppdb = PandasPdb()
    for pdb_file in os.scandir(input_folder):
        if pdb_file.is_file():
            pdb_path = pdb_file.path
            # We used the files that end with .pdb
            if pdb_path.endswith(".pdb"):

                output_path = output_folder + "/" + pdb_file

                # read pdb file with biopandas
                ppdb.read_pdb(pdb_path)
                ## the a and b repeated residiu are in column alt_loc, in here we take only the ones that are not
                # = to B i.e. we are deleting all the B
                ppdb.df["ATOM"] = ppdb.df["ATOM"][ppdb.df["ATOM"]["alt_loc"] != "B"]
                # Now we delete the column alt_loc because I found out later that it might move the text and then we
                # have later on problems converting the pdb to pbdbqt
                ppdb.df["ATOM"]["alt_loc"] = ""
                ppdb.to_pdb(
                    path=output_path, records=None, gz=False, append_newline=True
                )
