from ligands.rename_ligands import rename_ligands
from proteins.step1.PDB_info_extraction import pdb_info_extraction
from proteins.step2.exec_prepare_receptors import prepare_receptors
from proteins.step2.split_chains import split_chains
from proteins.step2.split_repeated_residues import split_repeated_residues
from proteins.step3.create_gridbox import create_gridbox
from ligands.extract_3D_structures import extract_3d_structures
from ligands.sdf_to_pdbqt import sdf_to_pdbqt
from ligands.exec_prepare_ligands import exec_prepare_ligands


if __name__ == "__main__":
    # make all folders if they don't exist

    # proteins
    # step 1: select and download pdbs; extract pdb info and save into an excel file.
    print("---------------- PROTEINS ----------------")
    print("################# STEP 1 #################")
    print("------------------------------------------")
    pdb_info_extraction()

    # step 2: split chains and remove waters, repeated and non-standard residues and alternative locations, convert .pdb files into .pdbqt files.
    print("---------------- PROTEINS ----------------")
    print("################# STEP 2 #################")
    print("------------------------------------------")
    split_chains()
    split_repeated_residues()
    prepare_receptors()

    # step 3: create a gridbox for each pdbqt file
    print("---------------- PROTEINS ----------------")
    print("################# STEP 3 #################")
    print("------------------------------------------")
    create_gridbox()

    print("----------- PROTEINS: COMPLETED ----------")
    # ligands
    # step 1: extract ligand structure but in sdf
    print("---------------- LIGANDS -----------------")
    print("################# STEP 1 #################")
    print("------------------------------------------")
    # extract_3d_structures()

    # step 2: convert sdf files into pdbqt
    print("---------------- LIGANDS -----------------")
    print("################# STEP 2 #################")
    print("------------------------------------------")
    # sdf_to_pdbqt()

    # step 3: convert pdb file to pdbqt, not necessary
    # exec_prepare_ligands()
    print("----------- LIGANDS: COMPLETED -----------")
