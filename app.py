from proteins.step1.PDB_info_extraction import pdb_info_extraction
from proteins.step2.split_chains import split_chains

if __name__ == "__main__":
    pdb_info_extraction()
    split_chains()
