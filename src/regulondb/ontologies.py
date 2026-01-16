"""
Ontology object.
Build data object from ontology object.
"""

# standard

# third party

# local


def get_only_properties_with_values(properties):
    properties = {key: value for key, value in properties.items() if value}
    return properties


def get_regulondb_ontologies(only_properties_with_values=False, ontology_owl_obj=None):
    from mco.domain.ontology import Ontology

    ontology = Ontology(
        ontology_owl_obj=ontology_owl_obj,
    )

    ontology_object = {
        "_id": ontology.obj_id,
        "citations": ontology.citations,
        "createdBy": ontology.created_by,
        "description": ontology.description,
        "externalCrossReferences": ontology.external_references,
        "iri": ontology.iri,
        "name": ontology.name,
        "note": ontology.notes,
        "ontologyCode": ontology.code,
        "versionIri": f'{ontology.ver_iri}',
        # TODO: Deprecated property "schemaVersion": ontology.schema_version,
    }

    if only_properties_with_values is True:
        ontology_object = get_only_properties_with_values(ontology_object)
    return ontology_object
