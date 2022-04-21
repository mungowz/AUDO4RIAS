import os
from config import Config


def rename_ligands(input_folder=Config.LIGANDS_SDF_FOLDER):

    for sdf_file in os.scandir(input_folder):
        if not sdf_file.is_file() or not sdf_file.path.endswith(".sdf"):
            continue
        # check if contains " "
        print("Renaming " + sdf_file.path)

        os.rename(sdf_file.path, sdf_file.path.replace(" ", "_"))
