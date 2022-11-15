from os import scandir
from os.path import join
from pathlib import Path
from subprocess import run
from shlex import quote
from Gui.windows.progressBar import indeterminateProgressBar

def performDocking(gridboxes_folder, proteins_folder, ligands_folder, outputs_folder):

    pb = indeterminateProgressBar(100, "Executing docking")
    pb.update()

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
                    
                    pb.increase()
                    pb.update()
