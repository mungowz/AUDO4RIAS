import os
from pathlib import Path
from filecmp import cmp
from config import Config

def delete_duplicates(
    ligands_folder = Config.LIGANDS_SDF_FOLDER
):
    DATA_DIR = Path(ligands_folder)
    files = sorted(os.listdir(DATA_DIR))
    duplicateFiles = []
    for file_x in files:
        if_dupl = False
        for class_ in duplicateFiles:
            if_dupl = cmp(
                DATA_DIR / file_x,
                DATA_DIR / class_[0],
                shallow = False
            )
            if if_dupl:
                class_.append(file_x)
                break
        if not if_dupl:
            duplicateFiles.append([file_x])
    print(duplicateFiles)