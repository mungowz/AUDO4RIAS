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

    # if we store data dict as csv file, we don't need to convert from .p to .csv, so we can plot data directly
    # we could store csv files into 'excel files' folder or into protein docking folder
    for root, dirs, files in os.walk(vina_folder):
        for file in files:
            if file.endswith("_contacts.p"):
                filepath = os.path.join(root, file)
                print(filepath)
                with open(filepath, 'rb+') as fp:
                    contact_states = pickle.load(fp)
                print(contact_states)
                print("\n\n\n\n\n")
                buildHeatmap(file.split(".")[0], contact_states, ligands, [res for res in contact_states.keys()])
                # pd.DataFrame(contact_states).to_csv(os.path.join(root, file.split(".")[0] + ".csv"))
    
    for root, dirs, files in os.walk(gnina_folder):
        for file in files:
            if file.endswith("_contacts.p"):
                filepath = os.path.join(root, file)
                with open(filepath, 'rb+') as fp:
                    contact_states = pickle.load(fp)
                print(contact_states)
                print("\n\n\n\n\n")
                buildHeatmap(file.split(".")[0], contact_states, ligands, [res for res in contact_states.keys()])
                # pd.DataFrame(contact_states).to_csv(os.path.join(root, file.split(".")[0] + ".csv"))
                
                
                 


