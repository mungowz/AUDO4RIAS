import os
from config import Config


def exec_prepare_ligands(
    pdb_folder=Config.LIGANDS_PDB_FOLDER, pdbqt_folder=Config.LIGANDS_PDBQT_FOLDER
):
    for pdb_file in os.scandir(pdb_folder):
        if pdb_file.is_file():
            pdb_path = pdb_file.path
            if pdb_path.endswith(".pdb"):
                pdb_code = pdb_path.split("\\")[-1].split(".")[0] + ".pdbqt"
                pdb_output = pdb_code + ".pdbqt"

                # WARNING: this output filename is not the exactly default output filename from prepare_receptor command
                output_filename = os.path.join(pdbqt_folder, pdb_code)

                #   command = 'prepare_ligand -l "' + pdb_path + '" -o "' + pdb_output + '"'
                command = 'obabel "' + pdb_path + '" -O "' + pdb_code + '"'
                print(command)

            # produce .pdbqt file for each pdb file
            os.system(command=command)
            break
