import os
import shutil

def pdb_to_pdbqt(pdb_folder, pdbqt_folder, verbose):
    for pdb_file in os.scandir(pdb_folder):
        os.chdir(pdb_folder)
        if pdb_file.is_file() and pdb_file.path.endswith(".pdb"):
            pdb_code = pdb_file.path.split(os.sep)[-1].split(".")[0]
            pdbqt_path = os.path.join(pdbqt_folder, pdb_code)       
            pdbqt_path = pdbqt_path + ".pdbqt"
            input_path = pdb_code.split(".")[0] + ".pdbqt"

            command = (
                'prepare_ligand' 
                + ' -l ' 
                + pdb_file.path
                + ' -v '
            )
            if verbose:
                print("Executing: " + command)
            os.system(command = command)
            print("\n")
            
            shutil.move(input_path, pdbqt_path)
            os.chdir(pdbqt_folder)
            for pdbqt_file in os.scandir(pdbqt_folder):
                if pdbqt_file.is_file() and pdbqt_file.path.endswith(".pdb"):
                    os.rename(pdbqt_file, "ligand_" + pdbqt_file)
