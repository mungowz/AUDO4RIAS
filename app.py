from proteins.step1.PDB_info_extraction import pdb_info_extraction
from proteins.step2.exec_prepare_receptors import prepare_receptors
from proteins.step2.split_chains import split_chains
from proteins.step2.split_repeated_residues import split_repeated_residues
from proteins.step3.create_gridbox import create_gridbox
from ligands.extract_3D_structures import extract_3D_structures
from ligands.delete_duplicates import delete_duplicates
from ligands.sdf_to_pdb import sdf_to_pdb


if __name__ == "__main__":
    # proteins
    # step 1: select and download pdbs; extract pdb info and save into an excel file.
    #pdb_info_extraction()

    # step 2: split chains and remove waters, repeated and non-standard residues and alternative locations.
    #split_chains()
    #   split_repeated_residues()
    #prepare_receptors()

    # step 3: create a gridbox for each pdbqt file
    #create_gridbox()

    # ligands
    # extract ligand structure but in sdf
    #extract_3D_structures()

    # delete duplicate into ligands folder
    delete_duplicates()

    #convert sdf files into pdb
    #sdf_to_pdb()


