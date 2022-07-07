import os


def pdb_to_pdbqt(pdb_folder, pdbqt_folder, verbose):
    for pdb_file in os.scandir(pdb_folder):
        os.chdir(pdb_folder)
        if pdb_file.is_file() and pdb_file.path.endswith(".pdb"):
            pdbqt_code = 'ligand_' + pdb_file.path.split(os.sep)[-1].split(".")[0] + '.pdbqt'
            pdbqt_path = os.path.join(pdbqt_folder, pdbqt_code) 

            command = (
                'prepare_ligand' 
                + ' -l ' 
                + pdb_file.path
                + ' -v '
                + ' -o '
                + pdbqt_path
            ) 
            if verbose:
                print("Executing: " + command)
            os.system(command = command)
            print("\n")
    