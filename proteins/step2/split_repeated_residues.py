from biopandas.pdb import PandasPdb
import os
from config import Config


def split_repeated_residues(
    input_folder=Config.PROTEINS_FOLDER, output_folder=Config.PROTEINS_FOLDER
):
    print("\n2.1 - Splitting repeated residues...")
    ppdb = PandasPdb()
    for pdb_file in os.scandir(input_folder):
        if not pdb_file.is_file() or not pdb_file.path.endswith(".pdb"):
            continue
        pdb_code = pdb_file.path.split("\\")[-1].split(".")[0]
        output_path = output_folder + "/" + pdb_code + ".pdb"

        # read pdb file with biopandas
        ppdb.read_pdb(pdb_file.path)

        ## the a and b repeated residues are in column alt_loc, in here we take only the ones that are not
        # = to B i.e. we are deleting all the B
        ppdb.df["ATOM"] = ppdb.df["ATOM"][ppdb.df["ATOM"]["alt_loc"] != "B"]

        # Now we delete the column alt_loc because I found out later that it might move the text and then we
        # have later on problems converting the pdb to pbdbqt
        ppdb.df["ATOM"]["alt_loc"] = ""
        ppdb.to_pdb(path=output_path, records=None, gz=False, append_newline=True)

    print("2.1 - Done.")
