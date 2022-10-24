from InteractionsAnalysis.interactionsVisualization import displayInteractions
from config import Config

import os


if __name__ == '__main__':

    vina_folder = Config.VINA_DOCKING_FOLDER
    gnina_folder =  Config.GNINA_DOCKING_FOLDER
    
    # For each protein-ligand complex, scores are stored in output/docking/<software>/<protein>/<ligand>/<protein>.p
    # For each protein-ligand complex, contacts are stored in output/docking/<software>/<protein>/<ligand>/<protein>_contacts.p
    # Overall scores are stored in output/docking/<software>/data.p
    # Overall contacts are stored in output/docking/<software>/contacts.p
    
    # choose a pickle file that stores scores
    # choose a pickle file that store contacts 
    # display interactions
    displayInteractions(os.path.join(vina_folder, 'data.p'), os.path.join(vina_folder, 'contacts.p'))
    displayInteractions(os.path.join(gnina_folder, 'data.p'), os.path.join(gnina_folder, 'contacts.p'))
    
    

