"""
Terms object.
Build data object from ontology object.
"""

# standard

# third party

# local


def get_only_properties_with_values(properties):
    properties = {key: value for key, value in properties.items() if value}
    return properties


def get_regulondb_terms(
        only_properties_with_values=False,
        ontology_owl_obj=None,
        ontology_code=None,
        base_iri=None
):
    from src.mco.domain.term import Term

    terms_list = []
    for term_class in list(ontology_owl_obj.classes()):
        term = Term(
            term_owl_class=term_class,
            ontology_code=ontology_code,
            base_iri=base_iri
        )

        term_object = {
            "_id": term.obj_id,
            "contributors": term.contributors,
            "description": term.description,
            "definition": term.definition,
            "externalCrossReferences": term.external_references,
            "hasDbXRef": term.has_db_cross_ref,
            "hasOboNameSpace": term.has_obo_name_space,
            "hasRelatedSynonyms": term.has_related_synonyms,
            "iri": term.iri,
            "name": term.name,
            "oboId": term.obo_id,
            "ontologies_id": term.ontologies_id,
            "subClassOf": term.sub_class_of,
            "superClassOf": term.super_class_of,
            "synonyms": term.synonyms,
            # TODO: Deprecated property "schemaVersion": ontology.schema_version,
        }
        if only_properties_with_values is True:
            term_object = get_only_properties_with_values(term_object)
        terms_list.append(term_object)
    return terms_list
