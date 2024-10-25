"""
Ontology object.
Build ontology object.
"""

# standard

# third party

# local


class Ontology(object):

    def __init__(self, **kwargs):
        # Params
        self.ontology_owl_obj = kwargs.get('ontology_owl_obj', None)

        # Local properties
        self.owl_metadata = kwargs.get('owl_metadata', None)

        # Object properties
        self.obj_id = kwargs.get('obj_id', None)
        self.citations = kwargs.get('citations', None)
        self.created_by = kwargs.get('created_by', None)
        self.description = kwargs.get('description', None)
        self.iri = kwargs.get('iri', None)
        self.external_references = kwargs.get('external_references', None)
        self.name = kwargs.get('name', None)
        self.notes = kwargs.get('notes', None)
        self.code = kwargs.get('code', None)
        self.ver_iri = kwargs.get('ver_iri', None)

    # Local properties
    @property
    def owl_metadata(self):
        return self._owl_metadata

    @owl_metadata.setter
    def owl_metadata(self, owl_metadata=None):
        if owl_metadata is None:
            owl_metadata = self.ontology_owl_obj.metadata
        self._owl_metadata = owl_metadata

    # Object properties
    @property
    def obj_id(self):
        return self._obj_id

    @obj_id.setter
    def obj_id(self, obj_id=None):
        if obj_id is None:
            obj_id = self.ontology_owl_obj.base_iri
        self._obj_id = obj_id

    @property
    def citations(self):
        return self._citations

    @citations.setter
    def citations(self, citations=None):
        if citations is None:
            citations = self.ontology_owl_obj.imported_citations
        self._citations = citations

    @property
    def created_by(self):
        return self._created_by

    @created_by.setter
    def created_by(self, created_by=None):
        if created_by is None:
            created_by = self.owl_metadata.contributor
        self._created_by = created_by

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description=None):
        if description is None:
            description = (
                self.owl_metadata.description[0] or
                None
            )
        self._description = description

    @property
    def iri(self):
        return self._iri

    @iri.setter
    def iri(self, iri=None):
        if iri is None:
            iri = (
                self.ontology_owl_obj.base_iri or
                ""
            )
        self._iri = iri

    @property
    def external_references(self):
        return self._external_references

    @external_references.setter
    def external_references(self, external_references=None):
        if external_references is None:
            external_reference = {
                "externalCrossReferences_id": "|ECOCYC|",
                "objectId": self.iri.replace("|", ""),
            }
            self._external_references = [external_reference]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if name is None:
            name = (
                self.owl_metadata.label[0] or
                None
            )
        self._name = name

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes=None):
        if notes is None:
            notes = (
                self.owl_metadata.IAO_0000116[0] or
                None
            )
        self._notes = notes

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code=None):
        if code is None:
            code = (
                self.owl_metadata.NCIT_NHC0[0] or
                None
            )
        self._code = code

    @property
    def ver_iri(self):
        return self._ver_iri

    @ver_iri.setter
    def ver_iri(self, ver_iri=None):
        if ver_iri is None:
            ver_iri = (
                self.owl_metadata.versionInfo[0] or
                None
            )
        self._ver_iri = ver_iri

    # Static methods
