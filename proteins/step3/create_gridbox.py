import Bio.PDB as bioPDB
import os
import pandas as pd
import openpyxl
from biopandas.pdb import PandasPdb
import math
from config import Config

# margin in anstroms to have some space between the max and min atom coordinates for the ligand
def create_gridbox(
    input_folder=Config.PROTEINS_FOLDER,
    output_folder=Config.GRIDBOX_OUTPUT,
    margin=3,
):
    ppdb = PandasPdb()

    print("3.1 - Creating gridbox for each pdbqt file...")
    for protein_file in os.scandir(input_folder):
        if protein_file.is_file():
            protein_path = protein_file.path
            # Now we use PandasPDB from the package biopandas to extract a table with the atom coordinates.
            # We used the files that end with .pdb
            if protein_path.endswith(".pdb"):
                # extract the protein_code from path name
                protein_code = protein_path.split("\\")[-1].split(".")[0]

                ppdb.read_pdb(protein_path)
                # With this lines we are extracting the code number from the proteins.
                # This is not use in this case, because we have split proteins in monomers and change the protein_code in some cases.
                # protein_code = ppdb.code
                # Now we are extractin the atom coodinastes
                atom = ppdb.df["ATOM"]
                # extract the min and max for x, y, z
                min_x = min(atom["x_coord"])
                max_x = max(atom["x_coord"])
                min_y = min(atom["y_coord"])
                max_y = max(atom["y_coord"])
                min_z = min(atom["z_coord"])
                max_z = max(atom["z_coord"])
                # To obtain the center, we do the average of min and max
                center_x = round((min_x + max_x) / 2, 3)
                center_y = round((min_y + max_y) / 2, 3)
                center_z = round((min_z + max_z) / 2, 3)
                # for the size we do the differences from max and min
                size_x = math.ceil(max_x - min_x) + margin
                size_y = math.ceil(max_y - min_y) + margin
                size_z = math.ceil(max_z - min_z) + margin
                # F means format. We are telling python that in this string we will introduce variables.
                # The variables will be the values ontained from the center and size.
                # Exhaustiveness is an input needed for vina. In this case we will use 16 but the standard is 8
                gridbox = f"""center_x = {center_x}
    center_y = {center_y}
    center_z = {center_z}

    size_x = {size_x}
    size_y = {size_y}
    size_z = {size_z}

    exhaustiveness = 16"""
                # to create the text with the grid box values, first we create the file name with the prot code + extension
                file_name = f"protein_{protein_code}_grid.txt"
                # Then we define the path of the output
                output_path = f"{output_folder}/{file_name}"
                # if protein_code == '1fcq':
                output = open(output_path, "w")
                output.write(gridbox)
                output.close()

                print(
                    "Gridbox created for " + protein_code + "! Stored in " + output_path
                )
