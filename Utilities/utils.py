import os
import gzip
import tempfile
import errno
import re
import pandas as pd
import pickle

def removeFiles(folder, docted_extension):
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


def checkFilesInFolder(folder, docted_extension):
    for files in os.scandir(folder):
        if files.path.endswith(docted_extension):
            return True
    return False



def saveDictToExcel(dict, folder):
    df = pd.DataFrame.from_dict(dict, orient="index")
    with pd.ExcelWriter(os.path.join(folder, "info_proteins.xlsx")) as writer:
        df.to_excel(
            writer,
            sheet_name="pdbs_selected",
            index=False,
        )
        # writer.save()




def mergeDicts(A, B, debug=False):
    if debug:
        print(A)
        print(B)
        print("len A: " + str(len(A))+", len B: " + str(len(B)))
        
    if len(A) == 0:
        A = B
        return A

    for key in B.keys():
        if key not in A.keys():
            A[key] = B[key]
            continue
        for contact, value in B[key].items():
            A[key][contact] = A[key].get(contact, 0) + B[key].get(contact, 0)

    if debug:
        print(A)
        print("\n\n\n")
    return A


def saveDictToPickle(docking_folder, dict):
    with open(os.path.join(docking_folder, "contacts.p"), 'wb+') as fp:
        pickle.dump(dict, fp, protocol=pickle.HIGHEST_PROTOCOL)




def getLigandsFromFolder(folder):
    ligands = []
    for root, dirs, files in os.walk(folder):
        for lig in files:
            if lig.endswith(".sdf") and lig.startswith("ligand_"):
                ligands.append(lig[lig.find("_")+1:-4])
    return ligands

        
def checkFilesExistance(paths):
    for path in paths:
        if not os.path.exists(path):
            return False
    return True

def checkRMSDCorrectness(rmsd):
    for value in rmsd:
        if value in [float("inf"), float(0)]:
            return False
    return True 


def findFile(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None