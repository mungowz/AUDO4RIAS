from utils import decompress
import os


def extract_remark350_monomeric(
    pdb_path,
    pdb_folder,
):
    keywords = [
        "AUTHOR DETERMINED BIOLOGICAL UNIT: MONOMERIC",
        "BIOLOGICAL UNIT: MONOMERIC",
    ]

    if pdb_path.endswith(".gz"):
        protein_code = pdb_path.split("\\")[-1].split(".")[0]
        output_path = os.path.join(pdb_folder, protein_code)
        # unzip .gz file
        decompress(pdb_path, output_path)

    # open pdb file
    with open(pdb_path, "r") as pdb_reader:
        pdb_data = pdb_reader.read()

    # search keywords in a textfile
    for keyword in keywords:
        if keyword in pdb_data:
            return True
    return False
