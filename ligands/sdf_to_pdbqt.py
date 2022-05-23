import os
from subprocess import call


def sdf_to_pdbqt(sdf_folder, pdbqt_folder, verbose):
    for sdf_file in os.scandir(sdf_folder):
        if sdf_file.is_file() and sdf_file.path.endswith(".sdf"):
            ligand_name = sdf_file.path.split(os.sep)[-1].split(".")[0]
            pdbqt_path = pdbqt_folder + "/ligand_" + ligand_name + ".pdbqt"

            command = ('obabel', sdf_file.path, '-O', pdbqt_path)
            call(command)
            if verbose:
                print(
                    "{ligand_name} converted from sdf into pdbqt! (Stored in {output_file})\n".format(
                        ligand_name=ligand_name, output_file=pdbqt_path
                    )
                )
