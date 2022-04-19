import os
import re
import pandas as pd
import pubchempy as pcp
from config import Config
import openpyxl


def extract_3D_structures(
    input_folder = Config.EXCEL_FOLDER,
    output_folder = Config.LIGANDS_SDF_FOLDER
):
    sheet = "Total_3D_structures"
    excel_path = input_folder + "\ligands_pubchem.xlsx"
    df_asEU = pd.read_excel(io = excel_path, sheet_name=sheet)
    substance_dict = dict()
    substance_noparent = dict() 
    substance_problem = dict()
    for substance in df_asEU["EU_database"]:
        structure = pcp.get_compounds(substance, "name", record_type = "3d")
        if structure != []:
            file_name = substance + ".sdf"
            path = output_folder + "/" + file_name
            pcp.download("SDF", path, substance, "name",record_type = "3d", overwrite = True)
            substance_dict[substance] = {"Substance": substance} 
        # if 3d not available, try again without ()
        if structure == []:
            substance_no_parenthesis = re.sub('(\(.*\))', "", substance).lstrip('-')
            structure2 = pcp.get_compounds(substance_no_parenthesis, "name", record_type = "3d")
            if structure2 != []:
                file_name = substance_no_parenthesis + ".sdf"
                path = output_folder + "/" + file_name
                pcp.download("SDF", path, substance_no_parenthesis, "name", record_type = "3d", overwrite = True)
                substance_noparent[substance] = {"Substance": substance,  "Substance_no_parenthesis": substance_no_parenthesis}
            if structure2 == []:
                substance_problem[substance] = {"Substance": substance, "Substance_no_parenthesis": substance_no_parenthesis}

    df_3d= pd.DataFrame.from_dict(substance_dict).transpose()   
    df_3dnoparent= pd.DataFrame.from_dict(substance_noparent).transpose()
    df_issues= pd.DataFrame.from_dict(substance_problem).transpose()
    writer = pd.ExcelWriter(excel_path, engine = "xlsxwriter")

    df_3d.to_excel(writer, sheet_name = "3D", index = False)
    df_3dnoparent.to_excel(writer, sheet_name = "3Dnoparent", index = False)
    df_issues.to_excel(writer, sheet_name = "issues", index = False)

    sheet = "Substance_Pubchem"
    df_issues = pd.read_excel(io = excel_path, sheet_name = sheet)
    df_pubchem = df_issues["pubchem_name"] 
    for substance in df_pubchem:
        structure = pcp.get_compounds(substance, "name", record_type = "3d")
        if structure != []:
            file_name = substance + ".sdf"
            path = output_folder + "/" + file_name
            pcp.download("SDF", path, substance, "name", record_type = "3d", overwrite = True)
            substance_dict[substance] = {"Substance": substance}
        if structure == []:
            substance_problem[substance] = {"Substance": substance}

    df_3d_2 = pd.DataFrame.from_dict(substance_dict).transpose()
    df_issues_2 = pd.DataFrame.from_dict(substance_problem).transpose()

    excel_book = openpyxl.load_workbook(excel_path)

    with pd.ExcelWriter(excel_path, engine = "openpyxl") as writer:
        writer.book = excel_book
        writer.sheets = {
            worksheet.title: worksheet
            for worksheet in excel_book.worksheets
        }
        df_3d_2.to_excel(writer, "3D_2", index = False)
        df_issues_2.to_excel(writer, "issues_2", index = False)
        writer.save()

