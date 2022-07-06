import os


def sdf_to_pdb(sdf_folder, pdb_folder, verbose):
    for sdf_file in os.scandir(sdf_folder):
        if sdf_file.is_file() and sdf_file.path.endswith(".sdf"):
            ligand_name = sdf_file.path.split(os.sep)[-1].split(".")[0]
            pdb_path = pdb_folder + "/" + ligand_name + ".pdb"
            
            command = (
                'obabel ' 
                + sdf_file.path 
                + ' -O '
                + pdb_path
            )
            os.system(command=command)

            if verbose:
                print(
                    "{ligand_name} converted from sdf into pdb! (Stored in {output_file})\n".format(
                        ligand_name=ligand_name, output_file=pdb_path
                    )
                )
