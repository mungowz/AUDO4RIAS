import os
from config import Config

def exec_prepare_ligands(
    input_folder=Config.LIGANDS_PDB_FOLDER,
    output_folder=Config.LIGANDS_PDBQT_FOLDER
):
    for pdb_file in os.scandir(input_folder):
        if pdb_file.is_file():
            pdb_path = pdb_file.path
            if pdb_path.endswith(".pdb"):
                pdb_code = (
                    "ligand_" + pdb_path.split("\\")[-1].split(".")[0] + ".pdbqt"
                )

                # WARNING: this output filename is not the exactly default output filename from prepare_receptor command
                output_filename = os.path.join(output_folder, pdb_code)

                command = (
                    "prepare_ligand -l "
                    + pdb_path
                    + "-v -o"
                    + output_filename
                )

            # produce .pdbqt file for each pdb file
            os.system(command=command)

