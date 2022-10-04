import pickle
from config import Config
from plot_interactions import build_heatmap, plot_interactions
import os
import pandas as pd



if __name__ == '__main__':
    vina_folder = Config.VINA_DOCKING_FOLDER
    gnina_folder = Config.GNINA_DOCKING_FOLDER

    filepath = os.path.join(vina_folder, "data.p") # data contains scores (number of close contacts, hydrogen bonds)

    # retrieve scores and contact states
    with open(filepath, 'rb') as fp:
        scores = pickle.load(fp)

    filepath = os.path.join(vina_folder, "contacts.p") # contacts contains for each residue the list of ligands involved in interactions
    with open(filepath, 'rb') as fp:
        contact_states = pickle.load(fp)

    plot_interactions(scores, contact_states)
    

