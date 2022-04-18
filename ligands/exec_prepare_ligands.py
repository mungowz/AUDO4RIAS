import os

input_folder = r"C:\Users\amung\OneDrive\Desktop\Tirocinio\Docking\ligands_PESTEU\ligands_pdb\From_sfd_2"
output_folder = r"C:\Users\amung\OneDrive\Desktop\Tirocinio\Docking\ligands_PESTEU\pdbqt2"

for pdb_file in os.scandir(input_folder):
        if pdb_file.is_file():
            pdb_path = pdb_file.path
            if pdb_path.endswith(".pdb"):
                pdb_code = (
                    "ligand_" + pdb_path.split("\\")[-1].split(".")[0] + ".pdbqt"
                )

                command = (
                    "prepare_ligand4.py -l "
                    + pdb_path
                    + "-v -o"
                    + pdb_code
                )

            # produce .pdbqt file for each pdb file
            os.system(command=command)

