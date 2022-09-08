import matplotlib.pyplot as plt
import numpy as np
import matplotlib

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
        
        ax.set_ylabel('Number of bonds')
        ax.set_title(protein)
        ax.set_xticks(x, residues)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        
        fig.tight_layout()
        plt.xticks(rotation=60)
        plt.show()


def build_heatmap(title, contact_states, ligands, residues):
      
    bond = []
    for res in range(len(residues)):
        contacts = []
        for lig in range(len(ligands)):
            try:
                if contact_states[residues[res]][ligands[lig]] == "hydrogen_bond":
                    contacts.append(255)
                else:
                    contacts.append(127)
            except KeyError:
                contacts.append(0)

        bond.append(contacts)

    bond = np.array(bond)
    # ligands_labels = [ligand[0:10]+".." if len(ligand) > 11 else ligand  for ligand in ligands]

    fig, ax = plt.subplots()
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(event):
        annot.xy = [int(event.xdata) , int(event.ydata)]
        text = 'x: {} and y: {} and contact: '.format(ligands[int(event.xdata)], residues[int(event.ydata)])
        
        try:
            contact = contact_states[residues[int(event.ydata)]][ligands[int(event.xdata)]]
        except KeyError:
            contact = "no bond"
        text += contact
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont = ax.contains(event)
            if cont:
                update_annot(event)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
    cid = fig.canvas.mpl_connect('motion_notify_event', hover)

    fig.set_dpi(100)
    im = ax.imshow(bond)
    ax.set_title(title)
    ax.set_ylabel("Residues")
    ax.set_xlabel("Ligands")
    # fig.tight_layout()
    fig.subplots_adjust(left=0.25, right=0.75)
    plt.show()
