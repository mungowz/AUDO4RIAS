import re
import pandas as pd
import pubchempy as pcp
from config import Config
import os


def extract_3d_structures(
    input_folder=Config.EXCEL_FOLDER,
    output_folder=Config.LIGANDS_SDF_FOLDER,
):

    ## for file in os.scandir():
    # os.remove(file)
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
            if not substance in ligands_list:
                ligands_list.append(substance)
                ligands_path = output_folder + "/" + substance + ".sdf"
                pcp.download(
                    "SDF", ligands_path, substance, "name", record_type="3d", overwrite=True
                )
                print(
                    "{ligands_code}.sdf downloaded! (Stored in {output_file})\n".format(
                        ligands_code=substance, output_file=ligands_path
                    )
                )
        if not structure:
            substance = re.sub("(\(.*\))", "", substance).lstrip("-")
            structure = pcp.get_compounds(
                substance, "name", record_type="3d"
            )
            if structure:
                if not substance in ligands_list:
                    ligands_list.append(substance)
                    ligands_no_parenthesis_list.append(substance)
                    ligands_path = output_folder + "/" + substance + ".sdf"
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
                    # os.rename
            if not structure:
                ligands_problem_list.append(substance)

    #extract ligands from Pubchem database
    for substance in df["Substance_Pubchem"]:
        structure = pcp.get_compounds(substance, "name", record_type="3d")
        if structure:
            if not substance in ligands_list:
                ligands_list.append(substance)
                ligands_path = output_folder + "/" + substance + ".sdf"
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
        if not structure:
            ligands_problem_list.append(substance)

    return[ligands_list, ligands_problem_list, ligands_no_parenthesis_list]