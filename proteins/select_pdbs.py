from rcsbsearch import Attr


def select_proteins(query_type, maximum_length, include_mutants):

    # unavailable pdbs from rcsb.org
    # 7ASD: removed because its pdb format is unavailable on rcsb.org. Maybe we can try to download pdb zipped format and unzip
    # 3R72: The coordinate for one atom was wrong and the atom was floating around too far away to create a bond. Assumed we have already the correct pdb in our input folder.
    pdbs_unavailable = ["3R72"]

    if query_type == "DEFAULT":
        scientific_name = Attr(
            "rcsb_entity_source_organism.scientific_name"
        ).exact_match("Apis mellifera")

        keywords = Attr("struct_keywords.pdbx_keywords").contains_words(
            "INHIBITOR, TOXIN, RNA, PEPTIDE, RIBOSOME"
        )
        length = Attr("entity_poly.rcsb_sample_sequence_length").greater_or_equal(
            maximum_length
        )
    elif query_type == "ALTERNATIVE":
        scientific_name = Attr(
            "rcsb_entity_source_organism.scientific_name"
        ).exact_match("Apis mellifera")
        keywords = Attr("struct_keywords.pdbx_keywords").contains_words("RIBOSOME")
        length = Attr("entity_poly.rcsb_sample_sequence_length").greater_or_equal(
            maximum_length
        )
    else:
        raise TypeError("Invalid query type...")

    mutants = Attr("entity_poly.rcsb_mutation_count").greater(0)
    if include_mutants is False:
        proteins_list = (scientific_name & ~keywords & length).exec().iquery()
    else:
        proteins_list = (
            (scientific_name & ~keywords & length & ~mutants).exec().iquery()
        )

    proteins_list = remove_unavailable_pdbs(
        pdbs_unavailable=pdbs_unavailable, pdbs_list=proteins_list
    )
    return proteins_list


def remove_unavailable_pdbs(pdbs_unavailable=[], pdbs_list=[]):
    for pdb in pdbs_unavailable:
        if pdb in pdbs_list:
            pdbs_list.remove(pdb)
    return pdbs_list
