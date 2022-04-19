from config import Config
from proteins.step1.decompress_gz import decompress


def extract_remark350_monomeric(
    pdb_path,
    output_folder=Config.PROTEINS_FOLDER,
):
    keywords = [
        "AUTHOR DETERMINED BIOLOGICAL UNIT: MONOMERIC",
        "BIOLOGICAL UNIT: MONOMERIC",
        "MONOMERIC",
    ]

    if pdb_path.endswith(".gz"):
        protein_code = pdb_path.split("\\")[-1].split(".")[0]
        output_path = output_folder + "/" + protein_code
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
