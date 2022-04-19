from rcsbsearch import Attr

# query to select Apis mellifera proteins:
#   - no peptides
#   - no RNA
def select_proteins():

    # unavailable pdbs from rcsb.org
    # 7ASD: removed because its pdb format is unavailable on rcsb.org. Maybe we can try to download pdb zipped format and unzip
    # 3R72: The coordinate for one atom was wrong and the atom was floating around too far away to create a bond. Assumed we have already the correct pdb in our input folder.
    pdbs_unavailable = ["7ASD", "3R72"]

    scientific_name = Attr("rcsb_entity_source_organism.scientific_name").exact_match(
        "Apis mellifera"
    )

    keywords = Attr("struct_keywords.pdbx_keywords").contains_words(
        "INHIBITOR, TOXIN, RNA, PEPTIDE, RIBOSOME"
    )

    proteins_list = (scientific_name & ~keywords).exec().iquery()
    proteins_list = remove_unavailable_pdbs(
        pdbs_unavailable=pdbs_unavailable, pdbs_list=proteins_list
    )

    print(proteins_list)
    print(len(proteins_list))

    return proteins_list


# def select_ribosome(maximum_length=60):
#    # unavailable pdbs from rcsb.org
#    pdbs_unavailable = ["7ASD", "3R72"]
#
#    text = (
#        Attr("rcsb_entity_source_organism.scientific_name")
#        .exact_match("Apis mellifera")
#        .and_("struct_keywords.pdbx_keywords")
#       .contains_words("RIBOSOME")
#        .and_("entity_poly.rcsb_sample_sequence_length")
#       .less(maximum_length)
#    )
#
#    ribosome_list = text.exec().iquery()
#    ribosome_list = remove_unavailable_pdbs(
#        pdbs_unavailable=pdbs_unavailable, pdbs_list=ribosome_list
#    )
#
#    print(ribosome_list)
#    print(len(ribosome_list))
#
#    return ribosome_list


def remove_unavailable_pdbs(pdbs_unavailable=[], pdbs_list=[]):
    for pdb in pdbs_unavailable:
        if pdb in pdbs_list:
            pdbs_list.remove(pdb)
    return pdbs_list
