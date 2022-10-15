import pandas as pd
import xlsxwriter
import pubchempy as pcp
import os
from Utilities.utils import removeFiles


def extract_3d_structures(excel_path, sdf_folder, excel_folder, verbose, keep_ligands):

    if not keep_ligands:
        removeFiles(sdf_folder, ".sdf")

    # select ligands from an excel file
    ### By default, ./excel_files/pest_group_MOA.xlsx ###
    sheet = "Hoja1"
    df = pd.read_excel(io=excel_path, sheet_name=sheet)
    # set of downloaded ligands
    ligands_set = set()
    # set of ligands that could not be downloaded
    ligands_problem_set = set()

    # extract ligands from Pubchem
    for substance in df["docking_ligand"]:
        ligands_path = os.path.join(sdf_folder, "ligand_" + substance + ".sdf")
        file_name = ligands_path
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