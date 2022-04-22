import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    PROTEINS_FOLDER = os.path.join(basedir, "proteins\proteins_files")
    QUERY_TYPE = "DEFAULT" or "ALTERNATIVE"
    EXCEL_FOLDER = os.path.join(basedir, "excel_files")
    GRIDBOX_OUTPUT = os.path.join(basedir, "proteins\gridbox_output")
    PDBQT_PROTEINS_FOLDER = os.path.join(basedir, "proteins\pdbqt")
    LIGANDS_SDF_FOLDER = os.path.join(basedir, "ligands\sdf")
    LIGANDS_PDB_FOLDER = os.path.join(basedir, "ligands\pdb")
    LIGANDS_PDBQT_FOLDER = os.path.join(basedir, "ligands\pdbqt")
