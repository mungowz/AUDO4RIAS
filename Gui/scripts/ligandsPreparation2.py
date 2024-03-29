from pubchempy import get_compounds, download
from xlsxwriter import Workbook
from os import sep, rename, scandir, chdir
import subprocess
import shlex
from os.path import join, exists
from Gui.windows.progressBar import determinateProgressBar


def selectLigands(sdf_folder, excel_folder, verbose, contents):
    
    # set of downloaded ligands
    ligands_set = set()
    # set of ligands that could not be downloaded
    ligands_problem_set = set()

    # extract ligands from Pubchem
    for substance in contents:
        substance = substance[:-1] + ""
        ligands_path = join(sdf_folder, "ligand_" + substance + ".sdf")
        file_name = ligands_path
        ligands_path = ligands_path.replace("(", "")
        ligands_path = ligands_path.replace(")", "")
        if not exists(file_name.replace(" ", "_")):
            structure = get_compounds(substance, "name", record_type="3d")
            if structure:
                ligands_set.add(substance)
                download(
                    "SDF",
                    ligands_path,
                    substance,
                    "name",
                    record_type="3d",
                    overwrite=True,
                )
                if verbose:
                    print(
                        "{ligands_code} downloaded! (Stored in {output_file})\n".format(
                            ligands_code=substance, output_file=ligands_path
                        )
                    )
                # replaces the space with the underscore in the name of the .sdf file
                rename(ligands_path, ligands_path.replace(" ", "_"))
            if not structure:
                if verbose:
                    print(
                        "{ligand_name} chemical name not matching with PubChem OR conformer generation is disallowed. Please check\n".format(
                            ligand_name=substance
                        )
                    )
                ligands_problem_set.add(substance)

    # write an output excel file which contains information about sdf ligands output
    workbook = Workbook(join(excel_folder, "ligands_sdf_output.xlsx"))
    worksheet_ligands = workbook.add_worksheet("ligands")
    worksheet_problem = workbook.add_worksheet("ligands_problem")
    
    # write dowloaded ligands
    for row_num, data in enumerate(ligands_set):
        worksheet_ligands.write(row_num, 0, data)
    
    # write ligands which could not be downloaded
    for row_num, data in enumerate(ligands_problem_set):
        worksheet_problem.write(row_num, 0, data)
    workbook.close()


def prepareLigands(pdb_folder, pdbqt_folder, verbose):

    for pdb_file in scandir(pdb_folder):
        chdir(pdb_folder)
        if pdb_file.is_file() and pdb_file.path.endswith(".pdb"):
            pdbqt_code = pdb_file.path.split(sep)[-1].split(".")[0] + '.pdbqt'
            pdbqt_path = join(pdbqt_folder, pdbqt_code) 

            command = [
                'prepare_ligand',
                '-l',
                shlex.quote(pdb_file.path),
                '-v', '-o',
                shlex.quote(pdbqt_path)
            ] 
            if verbose:
                print("Executing: " + " ".join(c for c in command))
            subprocess.run(command)
            print("\n")



def sdf2pdb(sdf_folder, pdb_folder, verbose):

    for sdf_file in scandir(sdf_folder):
        if sdf_file.is_file() and sdf_file.path.endswith(".sdf"):
            ligand_name = sdf_file.path.split(sep)[-1].split(".")[0]
            pdb_path = join(pdb_folder, ligand_name + ".pdb")
            command = [
                'obabel',
                shlex.quote(sdf_file.path),
                '-O',
                shlex.quote(pdb_path)
            ]
            print(" ".join(c for c in command))
            subprocess.run(command)


            if verbose:
                print(
                    "{ligand_name} converted from sdf into pdb! (Stored in {output_file})\n".format(
                        ligand_name=ligand_name, output_file=pdb_path
                    )
                )