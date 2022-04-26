import os
import gzip


def remove_files(folder, docted_extension):
    for file in os.scandir(folder):
        if file.is_file() and file.path.endswith(docted_extension):
            os.remove(file)


def decompress(infile, tofile):
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)
