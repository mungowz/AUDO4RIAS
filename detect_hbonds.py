from MolKit import Read
from MolKit.molecule import AtomSet, Atom
from MolKit.interactionDescriptor import InteractionDescriptor

# written in Python2

# took from Pmv -> displayCommands 
def print_macro_residue_contacts(intDescr):
        # print "\n\nresidues in 'receptor'-> 'ligand' residues in close contact"
        macro_res_d = intDescr.print_macro_residue_contacts(print_ctr=False)
        # print "\n"
        return [macro_res_d]


def print_ligand_residue_contacts(intDescr):
    # print "\n\nresidues in 'ligand'-> 'receptor' residues in close contact"
    lig_res_d = intDescr.print_ligand_residue_contacts(princ_ctr=False)
    # print "\n"
    return [lig_res_d]


def print_hydrogen_bonds(intDescr):
    print "\n\nhydrogen bonds (donor residue->acceptor residue(s))"
    hbonds_d = intDescr.print_hb_residue(print_ctr=False)
    print "\n"
    return [hbonds_d]


# took from Pmv -> hbondCommands -> writeIntermolHBonds.doit()
def writeIntermolHBonds(macro, lig, hbonds):

    nodes = macro.findType(Atom)
    if len(nodes)==0: return 'ERROR'

    hbats = AtomSet(nodes.get(lambda x: hasattr(x, 'hbonds')))
    if not hbats:
        print(macro.name + "@" + lig.name + ": no atoms with hbonds specified")
        return 'ERROR'
    bnds = []
    for at in hbats:
        for b in at.hbonds:

            # create hb dict {res : {at : value}}
            if b.donAt.top!=b.accAt.top and b not in bnds:
                if b.donAt.parent.name not in hbonds.keys():
                    hbonds[b.donAt.parent.name] = {}
                if b.donAt.name not in hbonds[b.donAt.parent.name].keys():
                    hbonds[b.donAt.parent.name][b.donAt.name] = 0
                hbonds[b.donAt.parent.name][b.donAt.name] += 1
                bnds.append(b)
    if not len(bnds):
        print(macro.name + "@" + lig.name + ": no intermolecular hydrogen bonds in specified atoms")
        return 'ERROR'



def detect_interactions(lig_filename, macro_filename, debug=False):
    # read ligand
    lig = Read(lig_filename) # "ligand_PNG_2cb3_a_out.pdbqt"
    lig = lig[0] # set to model1

    # read receptor
    macro = Read(macro_filename)[0] # "protein_2cb3_a.pdbqt"

    # build bonds
    macro.buildBondsByDistance()
    lig.buildBondsByDistance()

    # build interactions
    intDescr = InteractionDescriptor(lig, macro, percentCutoff=1.)
    macro.bindingSite = True # ??

    # show output on stdout
    hbonds_d = print_hydrogen_bonds(intDescr) # hydrogen bonds (i think closeContacts = res_no_hb + res_hb)
    close_res_d = print_macro_residue_contacts(intDescr) # close contacts macro -> ligand
    
    if debug: print(hbonds_d)
    if debug: print(close_res_d)
    if debug: intDescr.print_report()

    #writeIntermolHBonds
    # writeIntermolHBonds(macro, lig, hbonds)

    keylist = [
        'hydrogen_bonds',
        'close_contacts',
        'pi-pi interactions',
        'pi-cation interactions'
    ]

    # inspect hbonds_d
    residues = {}
    for bond in hbonds_d:
        for don,acc in bond.items():

            if debug:
                print("donor:")
                print(don)
                print("acceptor:")
                print(acc)
                print("1: " + don.parent.parent.name + " - 2: " + macro.name)

            if don.parent.parent.name == macro.name:
                if don.name not in residues.keys():
                    residues[don.name] = {}
                    residues[don.name]['hydrogen_bonds'] = 0
                residues[don.name]['hydrogen_bonds'] = residues[don.name].get('hydrogen_bonds', 0) + 1
            else:
                for res, value in acc.items():
                    if debug:
                        print("residue in acceptor: ")
                        print(res)
                    if res.name not in residues.keys():
                        residues[res.name] = {}
                        residues[res.name]['hydrogen_bonds'] = 0
                    residues[res.name]['hydrogen_bonds'] = residues[res.name].get('hydrogen_bonds', 0) + 1

            if debug:
                print("before close_contacts")
                print(residues)
    
    # inspect close contacts (res involved in hbonds included)
    for bond in close_res_d:
        for res,v in bond.items():
            if res.name not in residues.keys():
                residues[res.name] = {}
                residues[res.name]['close_contacts'] = 0
            
            residues[res.name]['close_contacts'] = residues[res.name].get('close_contacts', 0) + 1

    if debug:
        print("before eliminating; ")
        print(residues)


    # exclude hbonds res from close_contacts
    for res in residues.keys():
        try:
            residues[res]['close_contacts'] = residues[res].get('close_contacts', 0) - residues[res].get('hydrogen_bonds',0)
        except KeyError:
            continue



    if debug:
        print("after eliminating; ")
        print(residues)
    return residues


def merge(A, B, debug=False):
    if debug:
        print(A)
        print(B)
        print("len A: " + str(len(A))+", len B: " + str(len(B)))
        
    if len(A) == 0:
        A = B
        return A

    for key in B.keys():
        if key not in A.keys():
            A[key] = B[key]
            continue
        for contact, value in B[key].items():
            A[key][contact] = A[key].get(contact, 0) + B[key].get(contact, 0)

    if debug:
        print(A)
        print("\n\n\n")
    return A


from config import Config

if __name__ == "__main__":
    import os
    # initialize variables
    macro_folder = Config.PDBQT_PROTEINS_FOLDER
    docking_folder = Config.DOCKING_FOLDER

    proteins = {}

    # for each protein
    for root, dirs, files in os.walk(macro_folder):
        for macro in files:
            # extract protein code from macro
            protein_code = macro.split(".")[0].split("protein_")[-1]
            lig_folder = os.path.join(docking_folder, protein_code)
            macro_path = os.path.join(root, macro)

            proteins[protein_code] = {}
            # for each vina result stored in docking/<protein>/<ligand>/out.pdbqt
            for r, d, f in os.walk(lig_folder):
                for lig in f:
                    if lig == "out.pdbqt":
                        lig_path = os.path.join(r, lig)

                        # detect interactions
                        interaction = detect_interactions(lig_path, macro_path)
                        proteins[protein_code] = merge(proteins[protein_code], interaction)
                        

    print(proteins)


    # we are interested in all interactions.. so how can we deal with it?
    # sum(d.values()) to sum all values of a dictionary i.g. sum all residues involved in hbonds
    #{ "protein": 
    #   [
    #       { "residue": 
    #           { "hydrogen bonds" : value,
    #              "pi-pi interactions" : value,
    #              "pi-cation interactions" : value,
    #              "close_contacts" : value 
    #           }
    #       },
    #       ...
    #   ]
    #}




        
