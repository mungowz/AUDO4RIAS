import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def plot_interactions(scores, contact_states):
    proteins = [key for key in scores.keys()]

    for protein in proteins:
        residues = [key for key in scores[protein].keys()]
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
        x = np.arange(len(residues))
        width = 0.35

        fig, ax = plt.subplots()
    
        rects1 = ax.bar(x, close_contacts, width, label='close contacts')
        rects2 = ax.bar(x, hydrogen_bonds, width, bottom=close_contacts ,label='hydrogen bonds')
        
        ax.set_ylabel('Number of bonds')
        ax.set_title(protein, loc='left')
        ax.set_xticks(x, residues)
        ax.legend(loc='upper left')

        # ax.bar_label(rects1, padding=3)
        # ax.bar_label(rects2, padding=3)

        annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(bar, contact):
            x = bar.get_x()+bar.get_width()/2.
            y = bar.get_y()+bar.get_height()/2
            annot.xy = (x,y)

            # text = "{}".format(residues[int(bar.get_x()+bar.get_width()/2.)])

            # extract ligands
            ligs = [key for key, val in contact_states[protein][residues[int(bar.get_x()+bar.get_width()/2.)]].items() if val == contact]
            text = '\n'.join(ligs)
            
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(1)


        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                for bar in rects1:
                    cont, ind = bar.contains(event)
                    if cont:
                        update_annot(bar, contact="close_contact")
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                        return
                for bar in rects2:
                    cont, ind = bar.contains(event)
                    if cont:
                        update_annot(bar, contact="hydrogen_bond")
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                        return
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)
        # fig.tight_layout()
        fig.subplots_adjust(bottom=0.25, top=0.75)
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
                    bbox=dict(boxstyle="round", fc="w", alpha=1),
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
        annot.get_bbox_patch().set_alpha(1)


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
