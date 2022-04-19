import os
from config import Config


def prepare_receptors(
    input_folder=Config.PROTEINS_FOLDER, output_folder=Config.PDBQT_PROTEINS_FOLDER
):
    for pdb_file in os.scandir(input_folder):
        if pdb_file.is_file():
            pdb_path = pdb_file.path
            if pdb_path.endswith(".pdb"):
                pdb_code = (
                    "protein_" + pdb_path.split("\\")[-1].split(".")[0] + ".pdbqt"
                )

                # WARNING: this output filename is not the exactly default output filename from prepare_receptor command
                output_filename = os.path.join(output_folder, pdb_code)

                command = (
                    "prepare_receptor -r "
                    + pdb_path
                    + " -A checkhydrogens -U deleteAltB -U waters -e -o "
                    + output_filename
                )

            # produce .pdbqt file for each pdb file
            os.system(command=command)

            # 3r72: The coordinate for one atom was wrong and the atom was floating around too far away to create a bond
            # We assume that it is already correct in our input files
