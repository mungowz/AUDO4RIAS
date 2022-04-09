import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    PROTEINS_FOLDER = os.path.join(basedir, "proteins\proteins_files")
    RNA_FOLDER = os.path.join(basedir, "proteins\ribosome_files")
    POLIMER_ENTITY_TYPE = "PROTEINS" or "RNA"
    OUTPUT_FOLDER = os.path.join(basedir, "excel_files")
