import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    URL = "https://www.rcsb.org/search/advanced"
    PROTEINS_FOLDER = os.path.join(basedir, "proteins" + os.sep + "proteins_files")
    EXCEL_FOLDER = os.path.join(basedir, "excel_files")
    GRIDBOX_OUTPUT_FOLDER = os.path.join(basedir, "proteins"+ os.sep + "gridbox_output")
    PDBQT_PROTEINS_FOLDER = os.path.join(basedir, "proteins"+ os.sep + "pdbqt")
    LIGANDS_SDF_FOLDER = os.path.join(basedir, "ligands" + os.sep + "sdf")
    LIGANDS_PDB_FOLDER = os.path.join(basedir, "ligands"+ os.sep +  "pdb")
    LIGANDS_PDBQT_FOLDER = os.path.join(basedir, "ligands" + os.sep + "pdbqt")
