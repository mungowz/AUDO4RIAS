from prody import *
import os
from config import Config


def split_chains(input_folder=Config.PROTEINS_FOLDER):
    print("Splitting chains...")
    proteins_dict = {}
    for pdb_file in os.scandir(input_folder):
        if not pdb_file.is_file():
            continue

        protein_path = pdb_file.path
        if not protein_path.endswith(".pdb"):
            continue

        print("Parsing {pdb_file}...".format(pdb_file=pdb_file))
        print(protein_path)

        # parse pdb file, get AtomGroup object
        atoms = parsePDB(protein_path)

        print("Getting HierarchicalView for {pdb_file}".format(pdb_file=pdb_file))
        # generate Hierarchical View for AtomGroup object
        hv = atoms.getHierView()
        chids = list(set(atoms.getChids()))

        if hv.numChains() < 2:
            continue

        chid_sequence = {
            chids[chids.index("A")]: hv["A"].getSequence()
        }  # dict {chain-sequence}
        proteins_dict[atoms.getTitle()] = chid_sequence  # dict {code: {chain-sequence}}

        # for each chain starting from B, ...
        # compare sequence to a list of sequences for the same protein code, initially filled with chain A sequence
        # if sequence is not in the list then append chain and sequence to a dict for this protein code otherwise do nothing (chain will be splitted and deleted)

        # for each chain in hierarchical view
        for chid in chids:
            if chid == "A" or not hv[chid].getSequence():
                continue

            # for each chid-seq in {chain-sequence} for a given code
            for key in list(proteins_dict[atoms.getTitle()]):

                # compare sequence
                if hv[chid].getSequence() != proteins_dict[atoms.getTitle()][key]:

                    # add to dict
                    chid_sequence[chid] = hv[chid].getSequence()
                    proteins_dict[atoms.getTitle()] = chid_sequence

        for chid, seq in proteins_dict[atoms.getTitle()].items():

            # build new pdb filename
            filename = os.path.join(
                input_folder, atoms.getTitle() + "_{chid}".format(chid=chid)
            )

            print(filename)
            # parse a specific chain from a pdb file
            new_atoms = parsePDB(protein_path, chain=chid)

            # save new pdb file
            writePDB(filename, new_atoms)

        # remove old pdb file
        print("Deleting " + protein_path)
        os.remove(pdb_file)
    return [proteins_dict]
