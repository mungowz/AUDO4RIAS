from rcsbsearch import Attr

# query to select Apis mellifera proteins:
#   - no peptides
#   - no RNA
def select_proteins():
    scientific_name = Attr("rcsb_entity_source_organism.scientific_name").exact_match(
        "Apis mellifera"
    )
    text = Attr("entity_poly.rcsb_entity_polymer_type").exact_match("Protein")

    q3 = Attr("rcsb_polymer_instance_annotation.annotation_lineage.name").exact_match(
        "Peptides"
    )
    q4 = Attr("rcsb_polymer_instance_annotation.type").exact_match("SCOP")
    nested_attribute = ~q3 & q4

    proteins_list = (scientific_name & text & nested_attribute).exec().iquery()
    print(proteins_list)
    print(len(proteins_list))

    return proteins_list


def select_rna():
    text = (
        Attr("rcsb_entity_source_organism.scientific_name")
        .exact_match("Apis mellifera")
        .and_("entity_poly.rcsb_entity_polymer_type")
        .exact_match("RNA")
        .and_("entity_poly.rcsb_sample_sequence_length")
        .less(60)
    )

    rna_list = text.exec().iquery()
    print(rna_list)
    print(len(rna_list))
    return rna_list
