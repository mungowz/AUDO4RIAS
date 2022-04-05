from download_pdbs import download_proteins
from select_pdbs import select_rna
from select_pdbs import select_proteins

proteins_list = select_proteins()
rna_list = select_rna()

proteins_files = (
    r"C:\Users\Maax\computational-docking\Computational-Docking\proteins\proteins_files"
)
rna_files = (
    r"C:\Users\Maax\computational-docking\Computational-Docking\proteins\rna_files"
)

# download_proteins(proteins_list, proteins_files)
