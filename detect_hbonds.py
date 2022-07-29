from asyncore import write
from MolKit import Read
from MolKit.pdbParser import PdbqtParser
from MolKit.molecule import AtomSet, Atom
from MolKit.interactionDescriptor import InteractionDescriptor

# written in Python2

# took from Pmv -> displayCommands 
def print_macro_residue_contacts(intDescr):
        print "\n\nresidues in 'receptor'-> 'ligand' residues in close contact"
        intDescr.print_macro_residue_contacts()
        print "\n"


def print_ligand_residue_contacts(intDescr):
    print "\n\nresidues in 'ligand'-> 'receptor' residues in close contact"
    intDescr.print_ligand_residue_contacts()
    print "\n"


def print_hydrogen_bonds(intDescr):
    print "\n\nhydrogen bonds (donor residue->acceptor residue(s))"
    intDescr.print_hb_residue()
    print "\n"


# took from Pmv -> hbondCommands -> writeIntermolHBonds.doit()
def writeIntermolHBonds(macro):
    
    nodes = macro.findType(Atom)
    if len(nodes)==0: return 'ERROR'

    hbats = AtomSet(nodes.get(lambda x: hasattr(x, 'hbonds')))
    if not hbats:
        print 'no atoms with hbonds specified'
        return 'ERROR'
    bnds = []
    for at in hbats:
        for b in at.hbonds:
            if b.donAt.top!=b.accAt.top and b not in bnds:
                bnds.append(b)
    if not len(bnds):
        print 'no intermolecular hydrogen bonds in specified atoms'
        return 'ERROR'

    # write interactions into a file
    fptr = open("interactions", 'w')
    for b in bnds:
        outstring = ''+b.donAt.full_name() + ',' + b.accAt.full_name()
        if b.hAt is not None:
            outstring = outstring + ',' + b.hAt.full_name()
        outstring = outstring + '\n'
        fptr.write(outstring)
    fptr.close()


def detect_hbonds(lig_filename, macro_filename):
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
    print_ligand_residue_contacts(intDescr)
    print_macro_residue_contacts(intDescr)
    print_hydrogen_bonds(intDescr)


    #writeIntermolHBonds
    writeIntermolHBonds(macro)

detect_hbonds("ligand_PNG_2cb3_a_out.pdbqt", "protein_2cb3_a.pdbqt")