from ligands.extract_3D_structures import extract_3d_structures
from ligands.sdf_to_pdbqt import sdf_to_pdbqt
from ligands.exec_prepare_ligands import exec_prepare_ligands

def prepare_ligands():
    extract_3d_structures()
    sdf_to_pdbqt()
    #exec_prepare_ligands()
