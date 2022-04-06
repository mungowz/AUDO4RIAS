from download_pdbs import download_pdbs
from select_pdbs import select_ribosome
from select_pdbs import select_proteins

proteins_list = select_proteins()
ribosome_list = select_ribosome()

proteins_files = (
    r"C:\Users\Maax\computational-docking\Computational-Docking\proteins\proteins_files"
)
rna_files = (
    r"C:\Users\Maax\computational-docking\Computational-Docking\proteins\rna_files"
)

# download_pdbs(proteins_list, proteins_files)
