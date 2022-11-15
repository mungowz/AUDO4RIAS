from biopandas.pdb import PandasPdb
import os
import subprocess
import shlex
import math
from prody import *
import Bio.PDB as bioPDB
from config import Config
from MoleculesPreparation.structuresManipulation import extractRemark350Monomeric
from MoleculesPreparation.structuresSelection import RestApiSelection, downloadPdbs, selectPdbs
from Utilities.utils import saveDictToExcel, findFile

def deleteHeteroatomsChains(pdb_folder, verbose):
    if verbose:
        print("\nCleaning structures from heteroatoms chains...")
    pdb = PandasPdb()

    for pdb_file in os.scandir(pdb_folder):
        if not pdb_file.is_file() or not pdb_file.path.endswith(".pdb"):
            continue

        # read pdb file
        pdb.read_pdb(pdb_file.path)

        # get hetatm chains not in atom chains
        invalid_hetatm_chains = set(pdb.df["HETATM"]["chain_id"]) - set(
            pdb.df["ATOM"]["chain_id"]
        )

        # if hetatm chains is an empty set, continue
        if len(invalid_hetatm_chains) < 1:
            continue

        if verbose:
            print(
                "@" + pdb_file.path.split(os.sep)[-1] + ": detected invalid hetatm chains"
            )
            print(invalid_hetatm_chains)
        # for each record in HETATM dataframe of a given pdb, drop records in which chain_id is set to a chain in invalid_hetatm_chains
        for row in range(0, len(pdb.df["HETATM"].index)):
            if pdb.df["HETATM"]["chain_id"][row] not in invalid_hetatm_chains:
                continue

            line_idx = str(pdb.df["HETATM"]["line_idx"][row])
            pdb.df["HETATM"].drop([row], axis=0, inplace=True)
            if verbose:
                print(
                    "@"
                    + pdb_file.path.split(os.sep)[-1]
                    + ": record at row "
                    + line_idx
                    + " removed"
                )

        # save df as pdb in place
        pdb.to_pdb(path=pdb_file.path, records=None, gz=False, append_newline=True)

    print("Done.")




# margin in angstroms to have some space between the max and min atom coordinates for the ligand
def createGridboxes(pdb_folder, gridbox_output_folder, margin, verbose):
    ppdb = PandasPdb()

    if verbose:
        print("Creating the gridbox for each pdbqt file...")
    for protein_file in os.scandir(pdb_folder):
        if protein_file.is_file():
            protein_path = protein_file.path
            # Now we use PandasPDB from the package biopandas to extract a table with the atom coordinates.
            # We used the files that end with .pdb
            if protein_path.endswith(".pdb"):
                output_path, protein_code = createGridbox(ppdb, protein_path, gridbox_output_folder, margin)

                
                if verbose:
                    print(
                        "Gridbox created for "
                        + protein_code
                        + "! (Stored in "
                        + output_path
                        + ")"
                    )

                
def createGridbox(ppdb, protein_path, gridbox_folder, margin):
    
    # extract the protein_code from path name
    protein_code = protein_path.split(os.sep)[-1].split(".")[0]
    ppdb.read_pdb(protein_path)
    # With this lines we are extracting the code number from the proteins.
    # This is not use in this case, because we have split proteins in monomers and change the protein_code in some cases.
    # protein_code = ppdb.code
    # Now we are extractin the atom coodinastes
    atom = ppdb.df["ATOM"]
    # extract the min and max for x, y, z
    min_x = min(atom["x_coord"])
    max_x = max(atom["x_coord"])
    min_y = min(atom["y_coord"])
    max_y = max(atom["y_coord"])
    min_z = min(atom["z_coord"])
    max_z = max(atom["z_coord"])
    # To obtain the center, we do the average of min and max
    center_x = round((min_x + max_x) / 2, 3)
    center_y = round((min_y + max_y) / 2, 3)
    center_z = round((min_z + max_z) / 2, 3)
    # for the size we do the differences from max and min
    size_x = math.ceil(max_x - min_x) + margin
    size_y = math.ceil(max_y - min_y) + margin
    size_z = math.ceil(max_z - min_z) + margin
    # F means format. We are telling python that in this string we will introduce variables.
    # The variables will be the values ontained from the center and size.
    # Exhaustiveness is an input needed for vina. In this case we will use 16 but the standard is 8
    gridbox = f"""center_x = {center_x}
center_y = {center_y}
center_z = {center_z}

size_x = {size_x}
size_y = {size_y}
size_z = {size_z}

exhaustiveness = 16"""
    # to create the text with the grid box values, first we create the file name with the prot code + extension
    file_name = f"protein_{protein_code}_grid.txt"
    # Then we define the path of the output
    output_path = f"{gridbox_folder}/{file_name}"
    # if protein_code == '1fcq':
    output = open(output_path, "w")
    output.write(gridbox)
    output.close()
    return [output_path, protein_code]

def splitRepeatedResidues(pdb_folder, verbose, output_folder=None):
    if output_folder is None:
        output_folder = pdb_folder
    if verbose:
        print("\nSplitting repeated residues...")
    ppdb = PandasPdb()
    for pdb_file in os.scandir(pdb_folder):
        if not pdb_file.is_file() or not pdb_file.path.endswith(".pdb"):
            continue
        pdb_code = pdb_file.path.split(os.sep)[-1].split(".")[0]
        output_path = os.path.join(output_folder, pdb_code + ".pdb")

        # read pdb file with biopandas
        ppdb.read_pdb(pdb_file.path)

        ## the a and b repeated residues are in column alt_loc, in here we take only the ones that are not
        # = to B i.e. we are deleting all the B
        ppdb.df["ATOM"] = ppdb.df["ATOM"][ppdb.df["ATOM"]["alt_loc"] != "B"]

        # Now we delete the column alt_loc because I found out later that it might move the text and then we
        # have later on problems converting the pdb to pbdbqt
        ppdb.df["ATOM"]["alt_loc"] = ""
        ppdb.to_pdb(path=output_path, records=None, gz=False, append_newline=True)

    if verbose:
        print("Done.")



def splitChains(pdb_folder, verbose):
    if not verbose:
        confProDy(verbosity="none")
    if verbose:
        print("\nSplitting chains of monomeric biological unit...")

    proteins_dict = {}
    monomeric_proteins = []
    for pdb_file in os.scandir(pdb_folder):
        if not pdb_file.is_file():
            continue

        protein_path = pdb_file.path
        if not protein_path.endswith(".pdb"):
            continue

        if verbose:
            print("\nParsing {pdb_file}...".format(pdb_file=pdb_file))
            print(protein_path)

        # extract "monomeric" keyword
        if not extractRemark350Monomeric(protein_path, pdb_folder=pdb_folder):
            continue
        monomeric_proteins.append(protein_path.split(os.sep)[-1].split(".")[0])
        # parse pdb file, get AtomGroup object
        atoms = parsePDB(protein_path)

        if verbose:
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
            if chid == "A" or hv[chid].getSequence() == "":
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
                pdb_folder, atoms.getTitle() + "_{chid}".format(chid=chid)
            )
            if verbose:
                print(filename)
            # parse a specific chain from a pdb file
            new_atoms = parsePDB(protein_path, chain=chid)

            # save new pdb file
            writePDB(filename, new_atoms)

        # remove old pdb file
        if verbose:
            print("Deleting " + protein_path)
        os.remove(pdb_file)
    if verbose:
        print("Done.")
    return [proteins_dict, monomeric_proteins]


def selectReceptors(
    pdb_folder, excel_folder, verbose
):

    if verbose:
        print("PROTEINS FOLDER: " + pdb_folder)
        print("EXCEL FOLDER: " + excel_folder)
        print("\nSelecting proteins...")

    proteins_list = RestApiSelection(Config.URL)

    # Build a query that select all needed proteins
    # proteins_list = selectPdbs(
    #     query_type=query_type,
    #     minimum_length=minimum_length,
    #     include_mutants=include_mutants,
    # )

    if verbose:
        print("Proteins selected:")
        print(proteins_list)
        print("Number of Proteins selected: " + str(len(proteins_list)))
        print("\nDowloading proteins...")
    # download pdb files from a list
    downloadPdbs(pdbs_list=proteins_list, output_path=pdb_folder, verbose=verbose)

    proteins = dict()
    parser = bioPDB.PDBParser(PERMISSIVE=True, QUIET=True)

    for protein_file in os.scandir(pdb_folder):
        # for each protein_code in proteins_list
        if protein_file.is_file():
            protein_path = protein_file.path
            if protein_path.endswith(".pdb"):
                protein_code = protein_path.split(os.sep)[-1].split(".")[0]

                # parser is the fuction that scans and extracts information of a file with a predifine format
                # we define parser as permissive (will not give any error) and quite = true so we don't have warnings

                # safe data extracted from parser
                data = parser.get_structure(protein_code, protein_path)

                name = data.header["name"]
                keywords = data.header["keywords"]
                function = data.header["head"]
                journal = data.header["journal"]
                compound = ""
                # Compound is a dictionary that we want to transform to a list
                for k, v in data.header["compound"].items():
                    for k2, v2 in v.items():
                        compound = compound + k + "_" + k2 + ":" + v2 + ";"

                proteins[protein_code] = {
                    "code": protein_code,
                    "name": name,
                    "keywords": keywords,
                    "function": function,
                    "journal": journal,
                    "compound": compound,
                }

    if verbose:
        print("\nStoring information into an excel file...")

    saveDictToExcel(proteins, excel_folder)
    if verbose:
        print("Stored into " + os.path.join(excel_folder, "info_proteins.xlsx"))



def prepareReceptors(pdb_folder, pdbqt_folder, verbose, charges_to_add='Kollman'):
    SCRIPT_FILENAME = "replacePrepareReceptor4.sh"
    script_path = findFile(SCRIPT_FILENAME, os.environ.get("HOME"))
    command = [
        '/bin/sh',
        shlex.quote(script_path)
    ]
    if verbose:
        print("\nReplacing ADFRsuite prepare_receptor4.py script...")
        command.append('-v')

    subprocess.run(['chmod', 'u+x', shlex.quote(script_path)], check=True)
    subprocess.run(command, check=True)

    if verbose:
        print(
            "\nConverting .pdb files into .pdbqt files using prepare_receptor..."
        )
    for pdb_file in os.scandir(pdb_folder):
        if not pdb_file.is_file() or not pdb_file.path.endswith(".pdb"):
            continue

        pdb_code = "protein_" + pdb_file.path.split(os.sep)[-1].split(".")[0] + ".pdbqt"

        # WARNING: this output filename is not the exactly default output filename from prepare_receptor command
        output_filename = os.path.join(pdbqt_folder, pdb_code)

        # Usage: prepare_receptor4.py -r filename
        #       Description of command...
        #   -r   receptor_filename
        #            supported file types include pdb,mol2,pdbq,pdbqs,pdbqt, possibly pqr,cif
        # Optional parameters:
        #  [-C]  charges to add type:
        #            'gasteiger': addition of gasteiger charges"
        #            'Kollman': addition of Kollman charges"
        #            (default is 'None' which means preserve all input charges ie do not add new charges)"
        #  [-A]  type(s) of repairs to make:
        #            'bonds_hydrogens': build bonds and add hydrogens
        #            'bonds': build a single bond from each atom with no bonds to its closest neighbor
        #            'hydrogens': add hydrogens
        #            'checkhydrogens': add hydrogens only if there are none already
        #            'None': do not make any repairs
        #             (default is 'None')
        #  [-U]  cleanup type:
        #            'nphs': merge charges and remove non-polar hydrogens
        #            'lps': merge charges and remove lone pairs
        #            'waters': remove water residues
        #            'nonstdres': remove chains composed entirely of residues of
        #            types other than the standard 20 amino acids
        #            'deleteAltB': remove XX@B atoms and rename XX@A atoms->XX
        #            (default is 'nphs_lps_waters_nonstdres')
        #  [-e]  delete every nonstd residue from any chain
        #            'True': any residue whose name is not in this list:
        #               ['CYS','ILE','SER','VAL','GLN','LYS','ASN',
        #                   'PRO','THR','PHE','ALA','HIS','GLY','ASP',
        #                   'LEU', 'ARG', 'TRP', 'GLU', 'TYR','MET',
        #                   'HID', 'HSP', 'HIE', 'HIP', 'CYX', 'CSS']
        #               will be deleted from any chain.
        #               NB: there are no  nucleic acid residue names at all
        #               in the list and no metals.
        #            (default is False which means not to do this)
        #
        command = [
            "prepare_receptor",
            "-r",
            shlex.quote(pdb_file.path),
            "-A", 
            "checkhydrogens",
            "-C",
            charges_to_add,
            "-e","-o",
            shlex.quote(output_filename)
        ]

        if verbose:
            print("Executing: " + " ".join(c for c in command))
        # produce .pdbqt file for each pdb file
        subprocess.run(command)

        # 3r72: The coordinate for one atom was wrong and the atom was floating around too far away to create a bond
        # We assume that it is already correct in our input files

    if verbose:
        print("Done.")
