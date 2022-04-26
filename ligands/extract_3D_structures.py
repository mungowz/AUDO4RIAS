import re
import pandas as pd
import xlsxwriter
import pubchempy as pcp
import os
from utils import remove_files


def extract_3d_structures(excel_path, sdf_folder, excel_folder, verbose):

    remove_files(sdf_folder, ".sdf")

    # select ligands from an excel file
    ### By default, ./excel_files/ligands_pubchem.xlsx ###
    sheet = "Total_3D_structures"
    df = pd.read_excel(io=excel_path, sheet_name=sheet)
    # set of downloaded ligands
    ligands_set = set()
    # set of manipulated downloaded ligands
    ligands_no_parenthesis_set = set()
    # set of ligands that could not be downloaded
    ligands_problem_set = set()

    # extract ligands from EU database
    for substance in df["EU_database"]:
        structure = pcp.get_compounds(substance, "name", record_type="3d")
        if structure:
            if substance not in ligands_set:
                ligands_set.add(substance)
                ligands_path = os.path.join(sdf_folder, substance + ".sdf")
                file_name = ligands_path
                if not os.path.exists(file_name.replace(" ", "_")):
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
            # remove the brackets that could create problems in the name of the ligand
            substance = re.sub("(\(.*\))", "", substance).lstrip("-")
            structure = pcp.get_compounds(substance, "name", record_type="3d")
            if structure:
                if substance not in ligands_set:
                    ligands_set.add(substance)
                    ligands_no_parenthesis_set.add(substance)
                    ligands_path = os.path.join(sdf_folder, substance + ".sdf")
                    file_name = ligands_path
                    if not os.path.exists(file_name.replace(" ", "_")):
                        pcp.download(
                            "SDF",
                            ligands_path,
                            substance,
                            "name",
                            record_type="3d",
                            overwrite=True,
                        )

                        # replaces the space with the underscore in the name of the .sdf file
                        os.rename(ligands_path, ligands_path.replace(" ", "_"))

                        if verbose:
                            print(
                                "{ligands_code} downloaded! (Stored in {output_file})\n".format(
                                    ligands_code=substance, output_file=ligands_path
                                )
                            )
            if not structure:
                ligands_problem_set.add(substance)

    # extract ligands from Pubchem database
    for substance in df["Substance_Pubchem"]:
        structure = pcp.get_compounds(substance, "name", record_type="3d")
        if structure:
            if substance not in ligands_set:
                ligands_set.add(substance)
                ligands_path = os.path.join(sdf_folder, substance + ".sdf")
                file_name = ligands_path
                if not os.path.exists(file_name.replace(" ", "_")):
                    pcp.download(
                        "SDF",
                        ligands_path,
                        substance,
                        "name",
                        record_type="3d",
                        overwrite=True,
                    )

                    # replaces the space with the underscore in the name of the .sdf file
                    os.rename(ligands_path, ligands_path.replace(" ", "_"))

                    if verbose:
                        print(
                            "{ligands_code} downloaded! (Stored in {output_file})\n".format(
                                ligands_code=substance, output_file=ligands_path
                            )
                        )
        if not structure:
            ligands_problem_set.add(substance)

    # write an output excel file which contains information about sdf ligands output
    workbook = xlsxwriter.Workbook(
        os.path.join(excel_folder, "ligands_sdf_output.xlsx")
    )
    worksheet_ligands = workbook.add_worksheet("ligands")
    worksheet_no_parenthesis = workbook.add_worksheet("ligands_no_parenthesis")
    worksheet_problem = workbook.add_worksheet("ligands_problem")
    # write dowloaded ligands
    for row_num, data in enumerate(ligands_set):
        worksheet_ligands.write(row_num, 0, data)
    # write dowloaded ligands that have been manipulated
    for row_num, data in enumerate(ligands_no_parenthesis_set):
        worksheet_no_parenthesis.write(row_num, 0, data)
    # write ligands which could not be downloaded
    for row_num, data in enumerate(ligands_problem_set):
        worksheet_problem.write(row_num, 0, data)
    workbook.close()

    return [ligands_set, ligands_problem_set, ligands_no_parenthesis_set]
