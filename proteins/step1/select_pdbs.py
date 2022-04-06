from rcsbsearch import Attr

# query to select Apis mellifera proteins:
#   - no peptides
#   - no RNA
def select_proteins():
    scientific_name = Attr("rcsb_entity_source_organism.scientific_name").exact_match(
        "Apis mellifera"
    )

    keywords = Attr("struct_keywords.pdbx_keywords").contains_words(
        "INHIBITOR, TOXIN, RNA, PEPTIDE, RIBOSOME"
    )

    proteins_list = (scientific_name & ~keywords).exec().iquery()
    print(proteins_list)
    print(len(proteins_list))

    return proteins_list


def select_ribosome(maximum_length=60):
    text = (
        Attr("rcsb_entity_source_organism.scientific_name")
        .exact_match("Apis mellifera")
        .and_("struct_keywords.pdbx_keywords")
        .contains_words("RIBOSOME")
        .and_("entity_poly.rcsb_sample_sequence_length")
        .less(maximum_length)
    )

    ribosome_list = text.exec().iquery()
    print(ribosome_list)
    print(len(ribosome_list))

    return ribosome_list
