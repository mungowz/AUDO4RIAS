import Bio.PDB as bioPDB
import os
import pandas as pd
from proteins.download_pdbs import download_pdbs
from proteins.select_pdbs import select_proteins


def pdb_info_extraction(
    query_type, minimum_length, include_mutants, pdb_folder, excel_folder, verbose
):

    if verbose:
        print("\nQUERY_TYPE: " + query_type)
        print("PROTEINS FOLDER: " + pdb_folder)
        print("EXCEL FOLDER: " + excel_folder)
        print("\n1.1 - Selecting proteins...")
    # Build a query that select all needed proteins
    proteins_list = select_proteins(
        query_type=query_type,
        minimum_length=minimum_length,
        include_mutants=include_mutants,
    )
    if verbose:
        print("Proteins selected:")
        print(proteins_list)
        print("Number of Proteins selected: " + str(len(proteins_list)))
        print("\n1.2 - Dowloading proteins...")
    # download pdb files from a list
    download_pdbs(pdbs_list=proteins_list, output_path=pdb_folder, verbose=verbose)

    proteins = dict()
    parser = bioPDB.PDBParser(PERMISSIVE=True, QUIET=True)

    for protein_file in os.scandir(pdb_folder):
        # for each protein_code in proteins_list
        if protein_file.is_file():
            protein_path = protein_file.path
            if protein_path.endswith(".pdb"):
                protein_code = protein_path.split(os.sep)[-1].split(".")[0]

                # parser is the fuction that scans and extracts information of a file with a predifine format
                # we define parser as permissive (will not give any error) and quite = true so we don't have warnings

                # safe data extracted from parser
                data = parser.get_structure(protein_code, protein_path)

                name = data.header["name"]
                keywords = data.header["keywords"]
                function = data.header["head"]
                journal = data.header["journal"]
                compound = ""
                # Compound is a dictionary that we want to transform to a list
                for k, v in data.header["compound"].items():
                    for k2, v2 in v.items():
                        compound = compound + k + "_" + k2 + ":" + v2 + ";"

                proteins[protein_code] = {
                    "code": protein_code,
                    "name": name,
                    "keywords": keywords,
                    "function": function,
                    "journal": journal,
                    "compound": compound,
                }

    if verbose:
        print("\n1.3 - Storing information into an excel file...")
    df = pd.DataFrame.from_dict(proteins, orient="index")
    with pd.ExcelWriter(os.path.join(excel_folder, "info_proteins.xlsx")) as writer:
        df.to_excel(
            writer,
            sheet_name="pdbs_selected",
            index=False,
        )
        # writer.save()
    if verbose:
        print("Stored into " + os.path.join(excel_folder, "info_proteins.xlsx"))
