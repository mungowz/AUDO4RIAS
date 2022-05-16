from biopandas.pdb import PandasPdb
import os


def split_repeated_residues(pdb_folder, verbose, output_folder=None):
    if output_folder is None:
        output_folder = pdb_folder
    if verbose:
        print("\n2.1 - Splitting repeated residues...")
    ppdb = PandasPdb()
    for pdb_file in os.scandir(pdb_folder):
        if not pdb_file.is_file() or not pdb_file.path.endswith(".pdb"):
            continue
        pdb_code = pdb_file.path.split(os.sep)[-1].split(".")[0]
        output_path = os.path.join(output_folder, pdb_code + ".pdb")

        # read pdb file with biopandas
        ppdb.read_pdb(pdb_file.path)

        ## the a and b repeated residues are in column alt_loc, in here we take only the ones that are not
        # = to B i.e. we are deleting all the B
        ppdb.df["ATOM"] = ppdb.df["ATOM"][ppdb.df["ATOM"]["alt_loc"] != "B"]

        # Now we delete the column alt_loc because I found out later that it might move the text and then we
        # have later on problems converting the pdb to pbdbqt
        ppdb.df["ATOM"]["alt_loc"] = ""
        ppdb.to_pdb(path=output_path, records=None, gz=False, append_newline=True)

    if verbose:
        print("2.1 - Done.")
