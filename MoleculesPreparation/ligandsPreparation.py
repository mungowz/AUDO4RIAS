import pandas as pd
import xlsxwriter
import pubchempy as pcp
import os
import shlex
import subprocess
from Utilities.utils import removeFiles


def selectLigands(input_path, sdf_folder, excel_folder, verbose):
    
    # set of downloaded ligands
    ligands_set = set()
    # set of ligands that could not be downloaded
    ligands_problem_set = set()

    with open(input_path) as f:
        contents = f.readlines()
    f.close()

    # extract ligands from Pubchem
    for substance in contents:
        substance = substance[:-1] + ""
        ligands_path = os.path.join(sdf_folder, "ligand_" + substance + ".sdf")
        file_name = ligands_path
        ligands_path = ligands_path.replace("(", "_")
        ligands_path = ligands_path.replace(")", "_")
        if not os.path.exists(file_name.replace(" ", "_")):
            structure = pcp.get_compounds(substance, "name", record_type="3d")
            if structure:
                ligands_set.add(substance)
                pcp.download(
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
                os.rename(ligands_path, ligands_path.replace(" ", "_"))
            if not structure:
                if verbose:
                    print(
                        "{ligand_name} chemical name not matching with PubChem OR conformer generation is disallowed. Please check\n".format(
                            ligand_name=substance
                        )
                    )
                ligands_problem_set.add(substance)
    # write an output excel file which contains information about sdf ligands output
    workbook = xlsxwriter.Workbook(
        os.path.join(excel_folder, "ligands_sdf_output.xlsx")
    )
    worksheet_ligands = workbook.add_worksheet("ligands")
    worksheet_problem = workbook.add_worksheet("ligands_problem")
    # write dowloaded ligands
    for row_num, data in enumerate(ligands_set):
        worksheet_ligands.write(row_num, 0, data)
    # write ligands which could not be downloaded
    for row_num, data in enumerate(ligands_problem_set):
        worksheet_problem.write(row_num, 0, data)
    workbook.close()

    return [ligands_set, ligands_problem_set]


def prepareLigands(pdb_folder, pdbqt_folder, verbose):
    for pdb_file in os.scandir(pdb_folder):
        os.chdir(pdb_folder)
        if pdb_file.is_file() and pdb_file.path.endswith(".pdb"):
            pdbqt_code = pdb_file.path.split(os.sep)[-1].split(".")[0] + '.pdbqt'
            pdbqt_path = os.path.join(pdbqt_folder, pdbqt_code) 

            command = [
                'prepare_ligand',
                '-l',
                shlex.quote(pdb_file.path),
                '-v', 
                '-o',
                shlex.quote(pdbqt_path)
            ] 
            if verbose:
                print("Executing: " + " ".join(c for c in command))
            subprocess.run(command)
            print("\n")
    