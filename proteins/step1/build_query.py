from rcsbsearch import Attr, rcsb_attributes as attrs, TextQuery
import requests


q1 = (
    Attr("rcsb_entity_source_organism.scientific_name")
    .exact_match("Apis mellifera")
    .exec()
    .iquery()
)
print(len(q1))
