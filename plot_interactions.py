import matplotlib.pyplot as plt
import numpy as np

def plot_interactions(scores):
    proteins = [key for key in scores.keys()]
    print(proteins)
    for protein in proteins:
        residues = [key for key in scores[protein].keys()]
        print(residues)

        close_contacts = []
        hydrogen_bonds = []
        for res in residues:

            if 'close_contacts' in scores[protein][res].keys():
                close_contacts.append(scores[protein][res]['close_contacts'])
            else:
                close_contacts.append(0)

            if 'hydrogen_bonds' in scores[protein][res].keys():
                hydrogen_bonds.append(scores[protein][res]['hydrogen_bonds'])
            else:
                hydrogen_bonds.append(0)

        # close_contacts = [scores[protein][res]['close_contacts'] for res in residues if 'close_contacts' in scores[protein][res].keys()]
        # hydrogen_bonds = [scores[protein][res]['hydrogen_bonds'] for res in residues if 'hydrogen_bonds' in scores[protein][res].keys()]
        print(close_contacts)
        print(hydrogen_bonds)
        x = np.arange(len(residues))
        width = 0.35

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, close_contacts, width, label='close contacts')
        rects2 = ax.bar(x + width/2, hydrogen_bonds, width, label='hydrogen bonds')
        
        ax.set_ylabel('Occurences')
        ax.set_title(protein)
        ax.set_xticks(x, residues)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        
        fig.tight_layout()
        plt.xticks(rotation=60)
        plt.show()
