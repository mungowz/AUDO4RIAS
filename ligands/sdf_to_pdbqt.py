import os
from config import Config


def sdf_to_pdbqt(
    input_folder=Config.LIGANDS_SDF_FOLDER, output_folder=Config.LIGANDS_PDBQT_FOLDER
):
    for sdf_file in os.scandir(input_folder):
        if sdf_file.is_file() and sdf_file.path.endswith(".sdf"):
            ligand_name = sdf_file.path.split("\\")[-1].split(".")[0]
            output_path = output_folder + "/ligand_" + ligand_name + ".pdbqt"

            command = "obabel " + sdf_file.path + " -O " + output_path
            print(ligand_name + ": ")
            os.system(command=command)
