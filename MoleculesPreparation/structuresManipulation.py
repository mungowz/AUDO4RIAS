import os


def extractRemark350Monomeric(
    pdb_path,
    pdb_folder,
):
    keywords = [
        "AUTHOR DETERMINED BIOLOGICAL UNIT: MONOMERIC",
        "BIOLOGICAL UNIT: MONOMERIC",
    ]

    #    if pdb_path.endswith(".gz"):
    #        protein_code = pdb_path.split(os.sep)[-1].split(".")[0]
    #        output_path = os.path.join(pdb_folder, protein_code)
    #        # unzip .gz file
    #        decompress(pdb_path, output_path)

    # open pdb file
    with open(pdb_path, "r") as pdb_reader:
        pdb_data = pdb_reader.read()

    # search keywords in a textfile
    for keyword in keywords:
        if keyword in pdb_data:
            return True
    return False


def checkWarnings(pdb_folder):

    ## pdb example ##
    ## REMARK 350 BIOMOLECULE: n
    ## REMARK 350 AUTHOR DETERMINED BIOLOGICAL UNIT: str1
    ## REMARK 350 SOFTWARE DETERMINED QUATERNARY STRUCTURE: str2

    print("Checking warnings...")
    # if str1 != str2 put a warning
    author_determined_biological_unit = None
    biomolecule = None
    software_determined_quaternary_structure = None

    for pdb_file in os.scandir(pdb_folder):

        if not pdb_file.is_file() or not pdb_file.path.endswith(".pdb"):
            continue
        with open(pdb_file.path, "r") as pdb_reader:
            for l_no, line in enumerate(pdb_reader):

                if "REMARK" in line:
                    remark = line.split(" ")[1]
                    if remark > "350":
                        break

                if "BIOMOLECULE" in line:
                    biomolecule = line.rstrip().split(" ")[-1]

                    continue

                if "AUTHOR DETERMINED BIOLOGICAL UNIT" in line:
                    author_determined_biological_unit = line.rstrip().split(" ")[-1]
                    continue

                if "SOFTWARE DETERMINED QUATERNARY STRUCTURE" in line:
                    software_determined_quaternary_structure = line.rstrip().split(" ")[
                        -1
                    ]

                if (
                    software_determined_quaternary_structure is not None
                    and software_determined_quaternary_structure
                    != author_determined_biological_unit
                ):
                    # put a warning
                    print(
                        "\nWARNING: @"
                        + pdb_file.path.split(os.sep)[-1]
                        + ":BIOMOLECULE: "
                        + biomolecule
                        + "\n"
                        + "AUTHOR DETERMINED BIOLOGICAL UNIT ("
                        + author_determined_biological_unit
                        + ") and SOFTWARE DETERMINED QUATERNARY STRUCTURE ("
                        + software_determined_quaternary_structure
                        + ") are not equal!"
                    )
                software_determined_quaternary_structure = None

def sdf2pdb(sdf_folder, pdb_folder, verbose):
    for sdf_file in os.scandir(sdf_folder):
        if sdf_file.is_file() and sdf_file.path.endswith(".sdf"):
            ligand_name = sdf_file.path.split(os.sep)[-1].split(".")[0]
            pdb_path = os.path.join(pdb_folder, ligand_name + ".pdb")
            command = (
                'openbabel.obabel ' 
                + '\"' + sdf_file.path + '\"' 
                + ' -O '
                + '\"' + pdb_path + '\"'
            )
            print(command)
            os.system(command=command)

            if verbose:
                print(
                    "{ligand_name} converted from sdf into pdb! (Stored in {output_file})\n".format(
                        ligand_name=ligand_name, output_file=pdb_path
                    )
                )

def removeRemarks(input_filepath, output_filepath):

    with open(input_filepath, 'r') as pdbqt_reader:
        lines = pdbqt_reader.readlines()
        with open(output_filepath, 'w') as pdbqt_writer:
            for line in lines:
                if "minimizedAffinity" in line:
                    continue
                pdbqt_writer.write(line)  

                
