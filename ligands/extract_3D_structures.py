import re
import pandas as pd
import pubchempy as pcp
from config import Config
from ligands.searchTree import SearchTree


def extract_3d_structures(
    input_folder=Config.EXCEL_FOLDER,
    output_folder=Config.LIGANDS_SDF_FOLDER,
):
    sheet = "Total_3D_structures"
    excel_path = input_folder + "\ligands_pubchem.xlsx"
    df = pd.read_excel(io=excel_path, sheet_name=sheet)
    file_tree = SearchTree()
    file_tree.insert("")

    for substance in df["EU_database"]:
        structure = pcp.get_compounds(substance, "name", record_type="3d")
        if structure:
            file_name = substance + ".sdf"
            if not file_tree.exists(file_name):
                file_tree.insert(file_name)
                path = output_folder + "/" + file_name
                pcp.download("SDF", path, substance, "name", record_type="3d", overwrite=True)
            if not structure:
                substance_no_parenthesis = re.sub('(\(.*\))', "", substance).lstrip('-')
                structure = pcp.get_compounds(substance_no_parenthesis, "name", record_type="3d")
                if structure:
                    if not file_tree.exist(file_name):
                        file_tree.insert(file_name)
                        file_name = substance_no_parenthesis + ".sdf"
                        path = output_folder + "/" + file_name
                        pcp.download("SDF", path, substance_no_parenthesis, "name", record_type="3d", overwrite=True)

    for substance in df["Substance_Pubchem"]:
        structure = pcp.get_compounds(substance, "name", record_type="3d")
        if structure:
            file_name = substance + ".sdf"
            if not file_tree.exists(file_name):
                file_tree.insert(file_name)
                path = output_folder + "/" + file_name
                pcp.download("SDF", path, substance, "name", record_type="3d", overwrite=True)
