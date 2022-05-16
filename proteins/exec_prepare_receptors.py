import os


def prepare_receptors(pdb_folder, pdbqt_folder, verbose):
    if verbose:
        print(
            "\n3.1 - Converting .pdb files into .pdbqt files using prepare_receptor..."
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
        command = (
            "prepare_receptor -r "
            + pdb_file.path
            + " -A checkhydrogens -e -o "
            + output_filename
        )

        if verbose:
            print("Executing: " + command)
        # produce .pdbqt file for each pdb file
        os.system(command=command)

        # 3r72: The coordinate for one atom was wrong and the atom was floating around too far away to create a bond
        # We assume that it is already correct in our input files

    if verbose:
        print("2.3 - Done.")
