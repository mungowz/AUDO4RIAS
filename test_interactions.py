import pickle
from config import Config
from plot_interactions import plot_interactions
import os


if __name__ == '__main__':
    # retrieve scores and contact states
    with open("vina/data.p", 'rb') as fp:
        scores = pickle.load(fp)

    # contacts contains for each residue the list of ligands involved in interactions
    with open("vina/contacts.p", 'rb') as fp:
        contact_states = pickle.load(fp)

    plot_interactions(scores, contact_states)
    
    

