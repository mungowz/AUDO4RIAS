import pandas as pd
import openpyxl
import pubchempy as pcp
from pubchempy import get_compounds
import re


def extract_3D_structures_EU():
    as_EU = r"C:\Users\amung\OneDrive\Desktop\Tirocinio\Docking\ligands_PESTEU\ActiveSubstances.xlsx"
    sheet = "approvedEU"
    df_asEU = pd.read_excel(io=as_EU, sheet_name=sheet)
    output_folder_pdb = r"C:\Users\amung\OneDrive\Desktop\Tirocinio\Docking\ligands_PESTEU\ligand_sdf\sdf_1"
    substance_dict = dict()
    # sometimes the name of pubchem and EUdata set is not matching because there is an explanation in ()
    # this dictionary will contain the cases for wich deleting the () was helpfull to retrieve the 3D structure
    substance_noparent = dict()
    #The susbtance from this category will move to substance_problem
    substance_problem = dict()
    for substance in df_asEU['Substance']:
        # check if 3D structure is available
        structure = get_compounds(substance, 'name', record_type='3d')
        # if 3D structures available, download and to dictionary
        if structure:
            file_name = substance + ".sdf"
            path = output_folder_pdb + "/" + file_name
            pcp.download('SDF', path, substance, 'name', record_type='3d', overwrite=True)
            substance_dict[substance] = {'Substance': substance}
        # if 3d not available, try again without ()
        if not structure:
            substance_no_parenthesis = re.sub('(\(.*\))', "", substance).lstrip('-')
            structure2 = get_compounds(substance_no_parenthesis, 'name', record_type='3d')
            if structure2:
                file_name = substance_no_parenthesis + ".sdf"
                path = output_folder_pdb + "/" + file_name
                pcp.download('SDF', path, substance_no_parenthesis, 'name', record_type='3d', overwrite=True)
                substance_noparent[substance] = {'Substance': substance,
                                                 'Substance_no_parenthesis': substance_no_parenthesis}
            if not structure2:
                substance_problem[substance] = {'Substance': substance,
                                                'Substance_no_parenthesis': substance_no_parenthesis}


def extract_3D_structures_pubchem():
    input_folder = r"C:\Users\amung\OneDrive\Desktop\Tirocinio\Docking\ligands_PESTEU\ligands_pubchem.xlsx"
    sheet = "issues_check"
    df_issues = pd.read_excel(io=input_folder, sheet_name=sheet)
    df_pubchem = df_issues['pubchem_name'].dropna()
    output_folder_pdb = r"C:\Users\amung\OneDrive\Desktop\Tirocinio\Docking\ligands_PESTEU\ligand_sdf\sdf"
    substance_dict = dict()
    # sometimes the name of pubchem and EUdata set is not matching because there is an explanation in ()
    # this dictionary will contain the cases for wich deleting the () was helpfull to retrieve the 3D structure
    substance_problem = dict()

    for substance in df_pubchem:
        # check if 3D structure is available
        structure = get_compounds(substance, 'name', record_type='3d')
        # if 3D structures available, download and to dictionary
        if structure:
            file_name = substance + ".sdf"
            path = output_folder_pdb + "/" + file_name
            pcp.download('SDF', path, substance, 'name', record_type='3d', overwrite=True)
            substance_dict[substance] = {'Substance': substance}
            #print(substance_dict[substance])
        # if 3d not available, try again without ()
        if not structure:
            substance_problem[substance] = {'Substance': substance}
            print(substance_problem[substance])

    df_3d_2 = pd.DataFrame.from_dict(substance_dict).transpose()
    df_issues_2 = pd.DataFrame.from_dict(substance_problem).transpose()
    excel_book = openpyxl.load_workbook(input_folder)

    with pd.ExcelWriter(input_folder, engine='openpyxl') as writer:
        writer.book = excel_book
        writer.sheets = {
            worksheet.title: worksheet
            for worksheet in excel_book.worksheets
        }
        df_3d_2.to_excel(writer, '3D_2', index=False)
        df_issues_2.to_excel(writer, 'issues_2', index=False)
        writer.save()
