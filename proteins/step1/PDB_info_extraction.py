import biopandas.pdb as bioPDB
import os
import pandas as pd
import download_proteins

# input folder
protein_folder = r"C:\Users\Maax\computational-docking\Computational-Docking\proteins\proteins_files"  # maybe put it in environment variables accessible from os module


# Build a query that select all needed proteins
proteins_list = []  # query output

# download pdb files from a list
download_proteins(proteins_list=proteins_list, protein_folder=protein_folder)


### maybe this could work to downlow protein sdtructures from RCSB from RCSBpdb
# pdbl.retrieve_pdb_file('1bh1', pdir = protein_files, file_format = 'pdb')

proteins = dict()

for protein_file in os.scandir(protein_folder):
    if protein_file.is_file():
        protein_path = protein_file.path
        if protein_path.endswith(".pdb"):
            protein_code = protein_path.split("\\")[-1].split(".")[0]

            # parser is the fuction that scans and extracts information of a file with a predifine format
            # we define parser as permissive (will not give any error) and quite = true so we don't have warnings
            parser = bioPDB.PDBParser(PERMISSIVE=True, QUIET=True)
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

df = pd.DataFrame.from_dict(proteins).transpose()

df.to_excel(
    r"C:\Users\cactus\Dropbox\Docking\bee_proteins\info proteins.xlsx", index=False
)
