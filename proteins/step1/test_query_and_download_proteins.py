from download_proteins import download_proteins
from select_proteins import select_proteins

proteins_list = select_proteins()

proteins_files = (
    r"C:\Users\Maax\computational-docking\Computational-Docking\proteins\proteins_files"
)

download_proteins(proteins_list, proteins_files)
