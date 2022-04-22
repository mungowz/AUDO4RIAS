import re
import pandas as pd
import pubchempy as pcp
from config import Config
import os


def extract_3d_structures(
    input_folder=Config.EXCEL_FOLDER,
    output_folder=Config.LIGANDS_SDF_FOLDER,
):
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
    ligands_list = list()
    ligands_no_parenthesis_list = list()
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
                    os.rename(ligands_path, ligands_path.replace(" ", "_"))
        if not structure:
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
                    os.rename(ligands_path, ligands_path.replace(" ", "_"))
        if not structure:
            ligands_problem_list.append(substance)

    df_ligands = pd.DataFrame(ligands_list)
    ligands_writer = pd.ExcelWriter('ligands_output.xlsx', engine='xlsxwriter')
    df_ligands.to_excel(ligands_writer, sheet_name='ligands', index=False)
    ligands_writer.save()

    df_ligands_no_parenthesis = pd.DataFrame(ligands_no_parenthesis_list)
    ligands_no_parenthesis_writer = pd.ExcelWriter('ligands_output.xlsx', engine='xlsxwriter')
    df_ligands_no_parenthesis.to_excel(ligands_no_parenthesis_writer, sheet_name='ligands_no_parenthesis', index=False)
    ligands_no_parenthesis_writer.save()

    df_ligands_problem = pd.DataFrame(ligands_problem_list)
    ligands_problem_writer = pd.ExcelWriter('ligands_output.xlsx', engine='xlsxwriter')
    df_ligands_problem.to_excel(ligands_problem_writer, sheet_name='ligands_problem', index=False)
    ligands_problem_writer.save()

    return[ligands_list, ligands_problem_list, ligands_no_parenthesis_list]
