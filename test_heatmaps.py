import pickle
from config import Config
from plot_interactions import build_heatmap
import os
import pandas as pd


if __name__ == '__main__':
    docking_folder = Config.VINA_DOCKING_FOLDER
    ligands_folder = Config.LIGANDS_SDF_FOLDER

    ligands = []
    for root, dirs, files in os.walk(ligands_folder):
        for lig in files:
            if lig.endswith(".sdf") and lig.startswith("ligand_"):
                ligands.append(lig[lig.find("_")+1:-4])


    # if we store data dict as csv file, we don't need to convert from .p to .csv, so we can plot data directly
    # we could store csv files into 'excel files' folder or into protein docking folder
    for root, dirs, files in os.walk(docking_folder):
        for file in files:
            if file.endswith("_contacts.p"):
                filepath = os.path.join(root, file)
                with open(filepath, 'rb+') as fp:
                    contact_states = pickle.load(fp)
                # print(contact_states)
                # print("\n\n\n\n\n")
                build_heatmap(file.split(".")[0], contact_states, ligands, [res for res in contact_states.keys()])
                # pd.DataFrame(contact_states).to_csv(os.path.join(root, file.split(".")[0] + ".csv"))
                
                 


