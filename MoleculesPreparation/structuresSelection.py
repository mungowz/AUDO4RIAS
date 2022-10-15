import os
from prody import confProDy, fetchPDB
from rcsbsearch import Attr
import json
from urllib.parse import unquote
import requests, requests.utils

from webView import webView


def downloadPdbs(pdbs_list, output_path, verbose):
    if not verbose:
        confProDy(verbosity="none")

    # download only pdb files that aren't already downloaded
    for protein_code in pdbs_list:
        for root, dirs, files in os.walk(output_path):
            output_file = os.path.join(output_path, protein_code + ".pdb")

            # fetch the PDB file from rcsb.org
            fetchPDB(protein_code, folder=output_path, compressed=False)
            print("\n")


# unavailable pdbs from rcsb.org
# 7ASD: removed because its pdb format is unavailable on rcsb.org. Maybe we can try to download pdb zipped format and unzip
# 3R72: The coordinate for one atom was wrong and the atom was floating around too far away to create a bond. Assumed we have already the correct pdb in our input folder.
pdbs_unavailable = ["3R72"]

def selectPdbs(query_type, minimum_length, include_mutants):
    if query_type == "DEFAULT":
        scientific_name = Attr(
            "rcsb_entity_source_organism.scientific_name"
        ).exact_match("Apis mellifera")

        keywords = Attr("struct_keywords.pdbx_keywords").contains_words(
            "INHIBITOR, TOXIN, RNA, PEPTIDE, RIBOSOME"
        )
        length = Attr("entity_poly.rcsb_sample_sequence_length").greater_or_equal(
            minimum_length
        )
    elif query_type == "ALTERNATIVE":
        scientific_name = Attr(
            "rcsb_entity_source_organism.scientific_name"
        ).exact_match("Apis mellifera")
        keywords = Attr("struct_keywords.pdbx_keywords").contains_words("RIBOSOME")
        length = Attr("entity_poly.rcsb_sample_sequence_length").greater_or_equal(
            minimum_length
        )
    else:
        raise TypeError("Invalid query type...")

    mutants = Attr("entity_poly.rcsb_mutation_count").greater(0)
    if include_mutants is True:
        proteins_list = (scientific_name & ~keywords & length).exec().iquery()
    else:
        proteins_list = (
            (scientific_name & ~keywords & length & ~mutants).exec().iquery()
        )

    proteins_list = removeUnavailablePdbs(
        pdbs_unavailable=pdbs_unavailable, pdbs_list=proteins_list
    )
    return proteins_list


def removeUnavailablePdbs(pdbs_unavailable=[], pdbs_list=[]):
    for pdb in pdbs_unavailable:
        if pdb in pdbs_list:
            pdbs_list.remove(pdb)
    return pdbs_list



def RestApiSelection(url):
    data = unquote(str(webView(url)).split("request=")[-1])

    try:
        qdict = json.loads(data)
    except requests.JSONDecodeError as e:
        print("Remember to search something!")
        exit(-1)


    del qdict["request_options"]["paginate"]
    qdict["request_options"]["return_all_hits"] = True

    response = requests.get(f"https://search.rcsb.org/rcsbsearch/v2/query?json={json.dumps(qdict)}").json()

    proteins_list = []
    for pdict in response["result_set"]:
        for key, val in pdict.items():
            if key == "identifier":
                proteins_list.append(val)

    proteins_list = removeUnavailablePdbs(pdbs_unavailable=pdbs_unavailable, pdbs_list=proteins_list)
    return proteins_list