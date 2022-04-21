import os
import pybel
from config import Config


def sdf_to_pdb(
    input_folder=Config.LIGANDS_SDF_FOLDER,
    output_folder=Config.LIGANDS_PDB_FOLDER
):
    for sdf_file in os.scandir(input_folder):
        if sdf_file.is_file() and sdf_file.path.endswith(".sdf"):
            ligand_name = sdf_file.path.split('\\')[-1].split(".")[0]
            output_path = output_folder + "/" + ligand_name + ".pdb"
            for mol in pybel.readfile("sdf", sdf_file.path):
                mol.write("pdb", output_path, overwrite=True)