from os import scandir
from os.path import join
from pathlib import Path
from subprocess import run
from shlex import quote
from Gui.windows.progressBar import indeterminateProgressBar
from Utilities.utils import checkFilesInFolder
from tkinter.messagebox import showerror


def performDocking(gridboxes_folder, proteins_folder, ligands_folder, outputs_folder):
    
    print("set gridbox folder to ", gridboxes_folder)
    print("set proteins folder to ", proteins_folder)
    print("set ligands folder to ", ligands_folder)
    print("set outputs folder to ", outputs_folder)

    #pb = indeterminateProgressBar(100, "Executing docking")
    #pb.update()

    if not checkFilesInFolder(folder=gridboxes_folder, docted_extension=".txt"):
        showerror("Error", "There's no txt file into gridbox folder")
        return

    if not checkFilesInFolder(folder=ligands_folder, docted_extension=".pdbqt"):
        showerror("Error", "There's no pdbqt file into ligands folder")
        return

    if not checkFilesInFolder(folder=proteins_folder, docted_extension=".pdbqt"):
        showerror("Error", "There's no pdbqt file into proteins folder")
        return

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
                    
                    #pb.increase()
                    #pb.update()
