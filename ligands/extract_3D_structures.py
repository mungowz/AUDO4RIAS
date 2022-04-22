import re
import pandas as pd
import xlsxwriter
import pubchempy as pcp
from config import Config
import os


def extract_3d_structures(
    input_folder=Config.EXCEL_FOLDER,
    output_folder=Config.LIGANDS_SDF_FOLDER,
):
    # input menu to choose whether previously downloaded ligands should be deleted
    loop = True
    while loop:
        user_choise = input("You want to delete the sdf files already saved? (Yes/No)\n")
        if user_choise in ["Y", "y", "Yes", "YES", "yes"]:
            #remove file saved previously into output folder
            for file in os.scandir(output_folder):
                os.remove(file)
            print("files removed")
            loop = False
        elif user_choise in ["N", "n", "No", "NO", "no"]:
            print("files not removed")
            loop = False
        else:
            print("invalid input")

    sheet = "Total_3D_structures"
    excel_path = input_folder + "\ligands_pubchem.xlsx"
    df = pd.read_excel(io=excel_path, sheet_name=sheet)
    # list of downloaded ligands 
    ligands_list = list()
    # list of manipulated downloaded ligands 
    ligands_no_parenthesis_list = list()
    # list of ligands that could not be downloaded
    ligands_problem_list = list()

    #extract ligands from EU database
    for substance in df["EU_database"]:
        structure = pcp.get_compounds(substance, "name", record_type="3d")
        if structure:
            if substance not in ligands_list:
                ligands_list.append(substance)
                ligands_path = output_folder + "/" + substance + ".sdf"
                file_name = ligands_path
                if not os.path.exists(file_name.replace(" ", "_")):
                    pcp.download(
                        "SDF", ligands_path, substance, "name", record_type="3d", overwrite=True
                    )
                    print(
                        "{ligands_code}.sdf downloaded! (Stored in {output_file})\n".format(
                            ligands_code=substance, output_file=ligands_path
                        )
                    )
                    # replaces the space with the underscore in the name of the .sdf file
                    os.rename(ligands_path, ligands_path.replace(" ", "_"))
        if not structure:
            # remove the brackets that could create problems in the name of the ligand
            substance = re.sub("(\(.*\))", "", substance).lstrip("-")
            structure = pcp.get_compounds(
                substance, "name", record_type="3d"
            )
            if structure:
                if substance not in ligands_list:
                    ligands_list.append(substance)
                    ligands_no_parenthesis_list.append(substance)
                    ligands_path = output_folder + "/" + substance + ".sdf"
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
                        print(
                            "{ligands_code}.sdf downloaded! (Stored in {output_file})\n".format(
                                ligands_code=substance, output_file=ligands_path
                            )
                        )
                        # replaces the space with the underscore in the name of the .sdf file
                        os.rename(ligands_path, ligands_path.replace(" ", "_"))
            if not structure:
                ligands_problem_list.append(substance)

    #extract ligands from Pubchem database
    for substance in df["Substance_Pubchem"]:
        structure = pcp.get_compounds(substance, "name", record_type="3d")
        if structure:
            if substance not in ligands_list:
                ligands_list.append(substance)
                ligands_path = output_folder + "/" + substance + ".sdf"
                file_name = ligands_path
                if not os.path.exists(file_name.replace(" ", "_")):
                    pcp.download(
                        "SDF", 
                        ligands_path, 
                        substance, 
                        "name", 
                        record_type="3d", 
                        overwrite=True
                    )
                    print(
                        "{ligands_code}.sdf downloaded! (Stored in {output_file})\n".format(
                            ligands_code=substance, output_file=ligands_path
                        )
                    )
                    # replaces the space with the underscore in the name of the .sdf file
                    os.rename(ligands_path, ligands_path.replace(" ", "_"))
        if not structure:
            ligands_problem_list.append(substance)

    # write an output excel file which contains information about sdf ligands output
    workbook = xlsxwriter.Workbook(output_folder + "ligands_sdf_output.xlsx")
    worksheet_ligands = workbook.add_worksheet("ligands")
    worksheet_no_parenthesis = workbook.add_worksheet("ligands_no_parenthesis")
    worksheet_problem = workbook.add_worksheet("ligands_problem")
    # write dowloaded ligands 
    for row_num, data in enumerate(ligands_list):
        worksheet_ligands.write(row_num, 0, data)
    # write dowloaded ligands that have been manipulated
    for row_num, data in enumerate(ligands_no_parenthesis_list):
        worksheet_no_parenthesis.write(row_num, 0, data)
    # write ligands which could not be downloaded
    for row_num, data in enumerate(ligands_problem_list):
        worksheet_problem.write(row_num, 0, data)
    workbook.close()

    return[ligands_list, ligands_problem_list, ligands_no_parenthesis_list]
