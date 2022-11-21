from os import scandir, access, R_OK
from os.path import join, exists
from pathlib import Path
from subprocess import run
from shlex import quote
from Utilities.utils import checkFilesInFolder, isWritable
from tkinter.messagebox import showerror
from sys import exit, argv, stdout, stderr
from getopt import getopt, GetoptError
from config import Config


if __name__ == "__main__":

    def usage():
        print("Usage: %s" % argv[0])

        print(
            "Optional parameters: \n \
            \t[-g] | [--gridbox-folder]: define a folder where gridboxes files are stored\n \
            \t[-p] | [--protein-folder]: define a folder where proteins files are stored\n \
            \t[-l] | [--ligand-folder]: define a folder where ligands files are stored\n \
            \t[-o] | [--output-folder]: define a folder where outputs files have to be or are stored\n \
            \t[-h] | [--help]: print usage" 
        )

    # process command arguments
    try:
        opt_list, args = getopt(
            argv[1:],
            "g:p:l:o:h",
            [
                "gridbox-folder",
                "protein-folder",
                "ligand-folder",
                "output-folder",
                "pdb-folder",
                "help",
            ],
        )
    except GetoptError as msg:
        stdout = stderr
        print("performDocking.py: %s" % msg)
        usage()
        exit(2)  # should create our own error handler

    # initialize environment
    print("----------- performDocking.py -----------")
    print("######### INITIALIZE ENVIRONMENT #########")
    print("------------------------------------------")

    # initialize variables
    gridboxes_folder = Config.GRIDBOX_FOLDER
    proteins_folder = Config.RECEPTORS_PDBQT_FOLDER
    ligands_folder = Config.LIGANDS_PDBQT_FOLDER
    outputs_folder = Config.VINA_DOCKING_FOLDER

    print("set gridbox folder to ", gridboxes_folder)
    print("set proteins folder to ", proteins_folder)
    print("set ligands folder to ", ligands_folder)
    print("set outputs folder to ", outputs_folder)

    for o, a in opt_list:

        if o in ("-g", "--gridbox-folder"):
            # verify path  (existance, permissions)
            # set path to input file = a
            if not exists(a):
                print("Specify a valid input file!")
                exit(1)
            if not access(a, R_OK):
                print("Modify file permission!")
                exit(1)
            gridboxes_folder = a

        if o in ("-l", "--ligands_folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to ligands folder = a
            ligands_folder = a

        if o in ("-p", "--proteins-folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to proteins folder = a
            proteins_folder = a

        if o in ("-o", "--outputs-folder"):
            # verify path (permissions)
            if not isWritable(a):
                print("Specify a valid directory or modify dir permission!")
                exit(1)
            # set path to outputs folder = a
            outputs_folder = a

        if o in ("-h", "--help"):
            usage()
            exit(0)

    print("set ligands folder to ", ligands_folder)
    print("set proteins folder to ", proteins_folder)
    print("set outputs folder to ", outputs_folder)

    # initialize folders
    if outputs_folder == Config.VINA_DOCKING_FOLDER:
        Path(Config.VINA_DOCKING_FOLDER).mkdir(parents=True, exist_ok=True)
    if ligands_folder == Config.LIGANDS_PDB_FOLDER:
        Path(Config.LIGANDS_PDB_FOLDER).mkdir(parents=True, exist_ok=True)
    if proteins_folder == Config.RECEPTORS_PDBQT_FOLDER:
        Path(Config.RECEPTORS_PDBQT_FOLDER).mkdir(parents=True, exist_ok=True)
    if gridboxes_folder == Config.GRIDBOX_FOLDER:
        Path(Config.GRIDBOX_FOLDER).mkdir(parents=True, exist_ok=True)

    gridboxes_files = scandir(gridboxes_folder)
    proteins_files = scandir(proteins_folder)
    ligands_files = scandir(ligands_folder)

    for gridbox, protein in zip(gridboxes_files, proteins_files):

        if protein.is_file() and protein.path.endswith(".pdbqt") and gridbox.is_file() and gridbox.path.endswith(".txt"):

            protein_dir = join(outputs_folder, protein.name.replace("protein_", "").split(".")[0])
            Path(protein_dir).mkdir(parents=True, exist_ok=True)

            for ligand in ligands_files:

                if ligand.is_file() and ligand.path.endswith(".pdbqt"):
                    ligands_dir = join(protein_dir, ligand.name.replace("ligand_", "").split(".")[0])
                    Path(ligands_dir).mkdir(parents=True, exist_ok=True)

                    output = join(ligands_dir, "out.pdbqt")
                    log = join(ligands_dir, "log.txt")
                            
                    command = [
                        "vina",
                        "--config", quote(gridbox.path),
                        "--receptor", quote(protein.path),
                        "--ligand", quote(ligand.path),
                        "--out", quote(output),
                        "--log", quote(log),
                    ]
                    run(command)
