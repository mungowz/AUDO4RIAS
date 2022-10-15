import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    URL = "https://www.rcsb.org/search/advanced"
    RECEPTORS_PDB_FOLDER = os.path.join(basedir, "data" + os.sep + "proteins" + os.sep + "pdb")
    RECEPTORS_PDBQT_FOLDER = os.path.join(basedir, "data" + os.sep + "proteins" + os.sep + "pdbqt")    
    EXCEL_FOLDER = os.path.join(basedir, "output" + os.sep + "excel_files")
    GRIDBOX_FOLDER = os.path.join(basedir, "data" + os.sep + "proteins" + os.sep + "gridbox")
    LIGANDS_SDF_FOLDER = os.path.join(basedir, "data" + os.sep + "ligands" + os.sep + "sdf")
    LIGANDS_PDB_FOLDER = os.path.join(basedir, "data" + os.sep + "ligands"+ os.sep +  "pdb")
    LIGANDS_PDBQT_FOLDER = os.path.join(basedir, "data" + os.sep + "ligands" + os.sep + "pdbqt")
    VINA_DOCKING_FOLDER = os.path.join(basedir, "vina/docking")
    GNINA_DOCKING_FOLDER = os.path.join(basedir, "gnina/docking")
