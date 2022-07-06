import os


def pdb_to_pdbqt(pdb_folder, pdbqt_folder, verbose):
    for pdb_file in os.scandir(pdb_folder):
        os.chdir(pdb_folder)
        if pdb_file.is_file() and pdb_file.path.endswith(".pdb"):
            pdb_code = pdb_file.path.split(os.sep)[-1].split(".")[0]
            pdbqt_path = os.path.join(pdbqt_folder, 'ligand_' + pdb_code) + '.pdbqt' 

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
    