import pickle
from InteractionsAnalysis.interactionsVisualization import buildHeatmap
from Utilities.utils import getLigandsFromFolder
from config import Config
import os
import pandas as pd




if __name__ == '__main__':
    vina_folder = Config.VINA_DOCKING_FOLDER
    ligands_folder = Config.LIGANDS_SDF_FOLDER
    gnina_folder = Config.GNINA_DOCKING_FOLDER

    ligands = getLigandsFromFolder(ligands_folder)
    receptors = ["1fcu", "2h8v", "3fe9", "4e81", "5xz3_A", "6lqk_B"]

    # if we store data dict as csv file, we don't need to convert from .p to .csv, so we can plot data directly
    # we could store csv files into 'excel files' folder or into protein docking folder
    for dir in os.listdir(vina_folder):
        if dir not in receptors:
            continue

        for root, dirs, files in os.walk(os.path.join(vina_folder, dir)):
            for file in files:
                if file.endswith("_contacts.p"):
                    filepath = os.path.join(root, file)
                    print(f"CONTACTS: {filepath}")
                    with open(filepath, 'rb+') as fp:
                        contact_states = pickle.load(fp)

                    buildHeatmap(file.split(".")[0], contact_states, ligands, [res for res in contact_states.keys()])
    
    for dir in os.listdir(gnina_folder):
        if dir not in receptors:
            continue
        for root, dirs, files in os.walk(os.path.join(gnina_folder, dir)):
            for file in files:
                if file.endswith("_contacts.p"):
                    filepath = os.path.join(root, file)
                    print(f"CONTACTS: {filepath}")
                    with open(filepath, 'rb+') as fp:
                        contact_states = pickle.load(fp)

                    buildHeatmap(file.split(".")[0], contact_states, ligands, [res for res in contact_states.keys()])

                
                
                 


