from proteins.step1.PDB_info_extraction import pdb_info_extraction
from proteins.step2.exec_prepare_receptors import prepare_receptors
from proteins.step2.split_chains import split_chains
from proteins.step3.create_gridbox import create_gridbox
from ligands import sdf_to_pdb


if __name__ == "__main__":
    # pdb_info_extraction()
    # split_chains()
    # prepare_receptors()
    #create_gridbox()
    sdf_to_pdb()