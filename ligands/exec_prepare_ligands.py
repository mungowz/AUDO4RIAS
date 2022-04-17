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
            
                # WARNING: this output filename is not the exactly default output filename from prepare_receptor command
                # Needed review
                output_filename = os.path.join(output_filename, pdb_code)

                command = (
                    "prepare_ligand.py -l "
                    + pdb_path
                    + output_filename
                )

            # produce .pdbqt file for each pdb file
            os.system(command=command)

