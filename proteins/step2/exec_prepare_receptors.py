import os
from config import Config


def prepare_receptors(
    input_folder=Config.PROTEINS_FOLDER, output_folder=Config.PDBQT_PROTEINS_FOLDER
):
    for pdb_file in os.scandir(input_folder):
        if pdb_file.is_file():
            pdb_path = pdb_file.path
            if pdb_path.endswith(".pdb"):
                pdb_code = pdb_path.split("\\")[-1].split(".")[0] + ".pdbqt"
                output_filename = os.path.join(output_folder, pdb_code)
                command = (
                    "prepare_receptor -r "
                    + pdb_path
                    + " -A checkhydrogens -U deleteAltB -U waters -e -o "
                    + output_filename
                )

            # produce .pdbqt file for each proteins
            os.system(command=command)
