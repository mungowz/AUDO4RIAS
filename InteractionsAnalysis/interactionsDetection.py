from __future__ import with_statement
import pickle
from MolKit import Read
from MolKit.molecule import AtomSet, Atom
from MolKit.interactionDescriptor import InteractionDescriptor
import os
# written in Python2

# took from Pmv -> displayCommands 
def print_macro_residue_contacts(intDescr):
        # print "\n\nresidues in 'receptor'-> 'ligand' residues in close contact"
        macro_res_d = intDescr.print_macro_residue_contacts(print_ctr=0)
        # print "\n"
        return [macro_res_d]


def print_ligand_residue_contacts(intDescr):
    # print "\n\nresidues in 'ligand'-> 'receptor' residues in close contact"
    lig_res_d = intDescr.print_ligand_residue_contacts(print_ctr=0)
    # print "\n"
    return [lig_res_d]


def print_hydrogen_bonds(intDescr):
    # print "\n\nhydrogen bonds (donor residue->acceptor residue(s))"
    hbonds_d = intDescr.print_hb_residue(print_ctr=0)
    # print "\n"
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

def mergeDicts(A, B, debug=False):
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

def detectInteractionsForResidues(lig_filename, macro_filename, contact_states, debug=False):
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
    hbonds_d = print_hydrogen_bonds(intDescr) # hydrogen bonds (close contacts = res_no_hb + res_hb)
    close_res_d = print_macro_residue_contacts(intDescr) # close contacts (macro -> ligand)
    
    
    if debug: print(hbonds_d)
    if debug: print(close_res_d)
    if debug: intDescr.print_report()

    residues = {}
    # inspect close contacts (res involved in hbonds included)
    for bond in close_res_d:
        if debug: print("LIGAND: "+lig_filename.split(os.sep)[-2])
        for res,v in bond.items():
            if res.name not in residues.keys():
                residues[res.name] = {}
            if res.name not in contact_states.keys():
                contact_states[res.name] = {}

            contact_states[res.name].update({lig_filename.split(os.sep)[-2]: "close_contact"})    
            residues[res.name]['close_contacts'] = residues[res.name].get('close_contacts', 0) + 1

    # inspect hbonds_d
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
                if don.name not in contact_states.keys():
                    contact_states[don.name] = {}
                    
                contact_states[don.name].update({lig_filename.split(os.sep)[-2]: "hydrogen_bond"})
                residues[don.name]['hydrogen_bonds'] = residues[don.name].get('hydrogen_bonds', 0) + 1

                # to work with hbonds for residue (as donor or acceptor), we consider donor residues of proteins in hbonds as close contacts
                # and then we remove this info when eliminating hbonds from close contacts
                residues[don.name]['close_contacts'] = residues[don.name].get('close_contacts', 0) + 1
            else:
                for res, value in acc.items():
                    if debug:
                        print("residue in acceptor: ")
                        print(res)
                    if res.name not in residues.keys():
                        residues[res.name] = {}
                    if res.name not in contact_states.keys():
                        contact_states[res.name] = {}
                    
                    contact_states[res.name].update({lig_filename.split(os.sep)[-2] : "hydrogen_bond"})    
                    residues[res.name]['hydrogen_bonds'] = residues[res.name].get('hydrogen_bonds', 0) + 1

            if debug:
                print("before close_contacts")
                print(residues)
    
    if debug:
        print("before eliminating; ")
        print(residues)


    # exclude hbonds res from close_contacts
    for res in residues.keys():
        try:          
            residues[res]['close_contacts'] = int(residues[res]['close_contacts']) - int(residues[res]['hydrogen_bonds'])
        except KeyError:
            continue

    if debug:
        print("after eliminating; ")
        print(residues)
    return residues

def detectInteractions(macro_folder, docking_folder):
    # check if macro folder exists or is empty
    print("RECEPTOR FOLDER: %s" % macro_folder)
    print("DOCKING FOLDER: %s" % docking_folder)
    proteins = {}
    contact_states = {}
    # for each protein
    for root, dirs, files in os.walk(macro_folder):
        for macro in files:
            # extract protein code from macro
            protein_code = macro.split(".")[0].split("protein_")[-1]
            lig_folder = os.path.join(docking_folder, protein_code)
            macro_path = os.path.join(root, macro)

            # TO DO: check if can access protein code docking folder and if exists corresponding vina docking output
            proteins[protein_code] = {}
            contact_states[protein_code] = {}

            # for each result stored in  output/docking/<software>/<protein>/<ligand>/out.pdbqt
            for r, d, f in os.walk(lig_folder):
                for lig in f:
                    if lig == "out_without_remarks.pdbqt":
                        lig_path = os.path.join(r, lig)

                        print("\nLIGAND: %s" % lig_path)

                        # detect interactions
                        interaction = detectInteractionsForResidues(lig_path, macro_path, contact_states[protein_code])
                        proteins[protein_code] = mergeDicts(proteins[protein_code], interaction)
            
            if not bool(proteins[protein_code]):
                del proteins[protein_code]
                del contact_states[protein_code]

            output_file = os.path.join(lig_folder, protein_code + ".p")
            contact_states_file =  os.path.join(lig_folder, protein_code + "_contacts.p")


            # we can: dict -> dataframe with pandas -> csv (data not serialized, much space required)
            try:
                with open(output_file, 'wb+') as fp1: 
                    pickle.dump(proteins[protein_code], fp1, protocol=pickle.HIGHEST_PROTOCOL)
            except IOError as e:
                print("WARNING: " + str(e))
                continue

            try:
                with open(contact_states_file, 'wb+') as fp2:
                    pickle.dump(contact_states[protein_code], fp2, protocol=pickle.HIGHEST_PROTOCOL)
            except IOError as e:
                print("WARNING: " + str(e))
                continue

    # we can: dict -> dataframe with pandas -> csv (data not serialized, much space required)
    # print(contact_states)
    try:
        with open(os.path.join(docking_folder, "contacts.p"), 'wb+') as fp:
            pickle.dump(contact_states, fp, protocol=pickle.HIGHEST_PROTOCOL)
    except IOError as e:
        print("WARNING: "+ str(e))

    # print(proteins)

    try:
        with open(os.path.join(docking_folder, 'data.p'), 'wb+') as fp:
            pickle.dump(proteins, fp, protocol=pickle.HIGHEST_PROTOCOL)
    except IOError as e:
        print("WARNING: "+str(e))

    for protein in proteins.keys():
        for residue in proteins[protein].keys():
            factor = 1.0/sum(proteins[protein][residue].values())
            for bond in proteins[protein][residue].keys():
                proteins[protein][residue][bond] = str(round(proteins[protein][residue][bond] * factor, 2)) 

    # print(proteins)
    try:
        with open(os.path.join(docking_folder, 'data_normalized.p'), 'wb+') as fp:
            pickle.dump(proteins, fp, protocol=pickle.HIGHEST_PROTOCOL)
    except IOError as e:
        print("WARNING: " + str(e))
    
    return [proteins, contact_states]
    

    # we are interested in all interactions.. so how can we deal with it?
    # sum(d.values()) to sum all values of a dictionary i.g. sum all residues involved in hbonds
    #
    # proteins: dict for storing info about number of bonds [close contacts, hydrogen bonds]
    # {
    #    { "protein": 
    #        { "residue": 
    #            { "hydrogen bonds" : value, 
    #               "close_contacts" : value,
    #            }
    #        },
    #        ...
    #    },
    #    ...
    # }


    # contact_states: dict to store for each residue-ligand of each protein the contact type [close contact, hydrogen bond]
    # {  
    #    { "protein":
    #        { "residue":
    #            { "ligand": [close_contact, hydrogen_bond, no_bond],
    #               ...
    #            }
    #        },
    #        ...
    #    },
    #    ...
    # }
    #
    #


