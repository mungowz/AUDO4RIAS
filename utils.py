import os
import gzip
import tempfile
import errno
import re

def remove_files(folder, docted_extension):
    for file in os.scandir(folder):
        if file.is_file() and file.path.endswith(docted_extension):
            os.remove(file)


def decompress(infile, tofile):
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)


def isWritable(path):
    try:
        testfile = tempfile.TemporaryFile(dir=path)
        testfile.close()
    except (OSError, IOError) as e:
        if e.errno == errno.EACCES:
            print("Cannot access to directory: " + path)
            return False
        if e.errno == errno.EEXIST:  # 13, 17
            print("Directory not exists: " + path)
            return False
        e.filename = path
        raise
    return True


def check_files_in_folder(folder, docted_extension):
    for files in os.scandir(folder):
        if files.path.endswith(docted_extension):
            return True
    return False

