from prody import parsePDB
from biopandas.pdb import PandasPdb
import os


def clear_hetatm(pdb_folder, verbose):
    if verbose:
        print("\n2.2 - Clearing heteroatoms...")
    pdb = PandasPdb()

    for pdb_file in os.scandir(pdb_folder):
        if not pdb_file.is_file() or not pdb_file.path.endswith(".pdb"):
            continue

        # read pdb file
        pdb.read_pdb(pdb_file.path)

        # get hetatm chains not in atom chains
        invalid_hetatm_chains = set(pdb.df["HETATM"]["chain_id"]) - set(
            pdb.df["ATOM"]["chain_id"]
        )

        # if hetatm chains is an empty set, continue
        if len(invalid_hetatm_chains) < 1:
            continue

        if verbose:
            print(
                "@" + pdb_file.path.split(os.sep)[-1] + ": detected invalid hetatm chains"
            )
            print(invalid_hetatm_chains)
        # for each record in HETATM dataframe of a given pdb, drop records in which chain_id is set to a chain in invalid_hetatm_chains
        for row in range(0, len(pdb.df["HETATM"].index)):
            if pdb.df["HETATM"]["chain_id"][row] not in invalid_hetatm_chains:
                continue

            line_idx = str(pdb.df["HETATM"]["line_idx"][row])
            pdb.df["HETATM"].drop([row], axis=0, inplace=True)
            if verbose:
                print(
                    "@"
                    + pdb_file.path.split(os.sep)[-1]
                    + ": record at row "
                    + line_idx
                    + " removed"
                )

        # save df as pdb in place
        pdb.to_pdb(path=pdb_file.path, records=None, gz=False, append_newline=True)

    print("2.2 - Done.")
