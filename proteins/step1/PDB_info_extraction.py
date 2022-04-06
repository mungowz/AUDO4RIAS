import Bio.PDB as bioPDB
import os
import pandas as pd
from proteins.step1.download_pdbs import download_pdbs
from config import Config
from proteins.step1.select_pdbs import select_proteins, select_ribosome


def pdb_info_extraction(
    polymer_entity_type=Config.POLIMER_ENTITY_TYPE,
    pdbs_folder=Config.PROTEINS_FOLDER,
    output_path=Config.OUTPUT_FOLDER,
):
    print(polymer_entity_type)
    print(pdbs_folder)
    print(output_path)
    # input folder
    # protein_folder = r"C:\Users\Maax\computational-docking\Computational-Docking\proteins\proteins_files"  # maybe put it in environment variables accessible from os module
    # rna_folder = r"C:\Users\Maax\computational-docking\Computational-Docking\proteins\rna_files"

    if polymer_entity_type in ["PROTEINS", "Proteins", "proteins"]:

        # Build a query that select all needed proteins
        proteins_list = select_proteins()

        # download pdb files from a list
        download_pdbs(pdbs_list=proteins_list, output_path=pdbs_folder)

    elif polymer_entity_type in ["RIBOSOME", "Ribosome", "ribosome"]:

        # Build a query that select all needed ribosome
        ribosome_list = select_ribosome()

        # download pdb files from a list
        download_pdbs(pdbs_list=ribosome_list, output_path=pdbs_folder)
    else:
        raise TypeError("Invalid select type")

    proteins = dict()
    parser = bioPDB.PDBParser(PERMISSIVE=True, QUIET=True)

    for protein_file in os.scandir(pdbs_folder):
        # for each protein_code in proteins_list
        if protein_file.is_file():
            protein_path = protein_file.path
            if protein_path.endswith(".pdb"):
                protein_code = protein_path.split("\\")[-1].split(".")[0]

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

    df = pd.DataFrame.from_dict(proteins, orient="index")
    with pd.ExcelWriter(os.path.join(output_path, "info_proteins.xlsx")) as writer:
        df.to_excel(
            writer,
            sheet_name="pdbs_selected",
            index=False,
        )
        writer.save()
