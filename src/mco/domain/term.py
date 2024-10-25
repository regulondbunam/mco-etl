"""
Term metadata object.
Build term object.
"""


# standard

# third party

# local


class Term(object):

    def __init__(self, **kwargs):
        # Params
        self.term_owl_class = kwargs.get('term_owl_class', None)
        self.ontology_code = kwargs.get('ontology_code', None)
        self.base_iri = kwargs.get('base_iri', None)

        # Local properties
        self.iri = kwargs.get('iri', None)
        self.label = kwargs.get('label', None)
        self.url_id = kwargs.get('url_id', None)

        # Object properties
        self.iri = kwargs.get('iri', None)
        self.obj_id = kwargs.get('obj_id', None)
        self.contributors = kwargs.get('contributors', None)
        self.description = kwargs.get('description', None)
        self.definition = kwargs.get('definition', None)
        self.external_references = kwargs.get('external_references', None)
        self.has_db_cross_ref = kwargs.get('has_db_cross_ref', None)
        self.has_obo_name_space = kwargs.get('has_obo_name_space', None)
        self.has_related_synonyms = kwargs.get('has_related_synonyms', None)
        self.name = kwargs.get('name', None)
        self.obo_id = kwargs.get('obo_id', None)
        self.ontologies_id = kwargs.get('ontologies_id', None)
        self.sub_class_of = kwargs.get('sub_class_of', None)
        self.super_class_of = kwargs.get('super_class_of', None)
        self.synonyms = kwargs.get('synonyms', None)

    # Local properties
    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label=None):
        if label is None:
            label = (
                    self.term_owl_class.label[0] or
                    ""
            )
        self._label = label

    @property
    def url_id(self):
        return self._url_id

    @url_id.setter
    def url_id(self, url_id=None):
        if url_id is None:
            url_id = (
                    self.iri.split("/")[-1].replace("_", ":") or
                    ""
            )
        self._url_id = url_id

    # Object properties
    @property
    def iri(self):
        return self._iri

    @iri.setter
    def iri(self, iri=None):
        if iri is None:
            iri = (
                    self.term_owl_class.iri or
                    ""
            )
        self._iri = iri

    @property
    def obj_id(self):
        return self._obj_id

    @obj_id.setter
    def obj_id(self, obj_id=None):
        if obj_id is None:
            obj_id = self.ontology_code + "|" + self.url_id + "|" + self.label
        self._obj_id = obj_id

    @property
    def contributors(self):
        return self._contributors

    @contributors.setter
    def contributors(self, contributors=None):
        if contributors is None:
            text = self.term_owl_class.createdBy + self.term_owl_class.created_by
            if text:
                text = (
                        text[0] or
                        None
                )
            creation_date = self.term_owl_class.creation_date
            if creation_date:
                creation_date = (
                        creation_date[0] or
                        None
                )
            contributors = {
                "text": text,
                "creation_date": creation_date,
            }
            contributors = Term.get_only_properties_with_values(contributors)
        self._contributors = contributors

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description=None):
        if description is None:
            description = (
                    str(
                        self.term_owl_class.description +
                        self.term_owl_class.MCO_0000382 +
                        self.term_owl_class.IAO_0000112
                    ).replace("[", "").replace("]", "") or
                    None
            )
        self._description = description

    @property
    def definition(self):
        return self._definition

    @definition.setter
    def definition(self, definition=None):
        if definition is None:
            definition_text = (
                    str(
                        self.term_owl_class.description +
                        self.term_owl_class.IAO_0000115 +
                        self.term_owl_class.MCO_0000851
                    ).replace("[", "").replace("]", "") or
                    None
            )
            definition_source = self.term_owl_class.IAO_0000119
            if definition_source:
                definition_source = (
                        definition_source[0] or
                        None
                )
            definition = {
                "text": definition_text,
                "source": definition_source
            }
            definition = Term.get_only_properties_with_values(definition)
        self._definition = definition

    @property
    def external_references(self):
        return self._external_references

    @external_references.setter
    def external_references(self, external_references=None):
        if external_references is None:
            external_reference = {
                "externalCrossReferences_id": "|ECOCYC|",
                "objectId": self.obj_id,
            }
            external_references = [external_reference]
        self._external_references = external_references

    @property
    def has_db_cross_ref(self):
        return self._has_db_cross_ref

    @has_db_cross_ref.setter
    def has_db_cross_ref(self, has_db_cross_ref=None):
        if has_db_cross_ref is None:
            has_db_cross_ref = (
                    self.term_owl_class.hasDbXref or
                    None
            )
        self._has_db_cross_ref = has_db_cross_ref

    @property
    def has_obo_name_space(self):
        return self._has_obo_name_space

    @has_obo_name_space.setter
    def has_obo_name_space(self, has_obo_name_space=None):
        if has_obo_name_space is None:
            has_obo_name_space = self.term_owl_class.hasOBONamespace
            if has_obo_name_space:
                has_obo_name_space = (
                        has_obo_name_space[0] or
                        None
                )
        self._has_obo_name_space = has_obo_name_space

    @property
    def has_related_synonyms(self):
        return self._has_related_synonyms

    @has_related_synonyms.setter
    def has_related_synonyms(self, has_related_synonyms=None):
        if has_related_synonyms is None:
            has_related_synonyms = (
                    self.term_owl_class.hasRelatedSynonym or
                    None
            )
        self._has_related_synonyms = has_related_synonyms

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if name is None:
            name = self.label
        self._name = name

    @property
    def obo_id(self):
        return self._obo_id

    @obo_id.setter
    def obo_id(self, obo_id=None):
        if obo_id is None:
            obo_id = self.url_id
        self._obo_id = obo_id

    @property
    def ontologies_id(self):
        return self._ontologies_id

    @ontologies_id.setter
    def ontologies_id(self, ontologies_id=None):
        if ontologies_id is None:
            ontologies_id = self.base_iri
        self._ontologies_id = ontologies_id

    @property
    def sub_class_of(self):
        return self._sub_class_of

    @sub_class_of.setter
    def sub_class_of(self, sub_class_of=None):
        if sub_class_of is None:
            sub_class_of_obj = self.term_owl_class.is_a
            sub_class_of_array = []
            for parent_obj in sub_class_of_obj:
                if str(parent_obj) == "owl.Thing":
                    # sub_class_of_array.append(str(parent_obj))
                    pass
                else:
                    if ".some(" not in str(parent_obj):
                        parent_label = parent_obj.label or None
                        parent_url_id = parent_obj.iri.split("/")[-1].replace("_", ":") or None
                        if parent_label and parent_url_id:
                            parent_id = self.ontology_code + "|" + parent_url_id + "|" + parent_label[0]
                            sub_class_of_array.append(parent_id)
            sub_class_of = sub_class_of_array
        self._sub_class_of = sub_class_of

    @property
    def super_class_of(self):
        return self._super_class_of

    @super_class_of.setter
    def super_class_of(self, super_class_of=None):
        if super_class_of is None:
            sup_class_of_obj = list(self.term_owl_class.subclasses())
            sup_class_of_array = []
            for child_obj in sup_class_of_obj:
                if ".some(" not in str(child_obj):
                    child_label = child_obj.label[0] or None
                    child_url_id = child_obj.iri.split("/")[-1].replace("_", ":") or None
                    if child_label and child_url_id:
                        child_id = self.ontology_code + "|" + child_url_id + "|" + child_label
                        sup_class_of_array.append(child_id)
            super_class_of = sup_class_of_array
        self._super_class_of = super_class_of

    @property
    def synonyms(self):
        return self._synonyms

    @synonyms.setter
    def synonyms(self, synonyms=None):
        if synonyms is None:
            synonyms = (
                    (
                            self.term_owl_class.hasExactSynonym +
                            self.term_owl_class.MCO_0000190
                    ) or
                    None
            )
        self._synonyms = synonyms

    # Static methods
    @staticmethod
    def get_only_properties_with_values(properties):
        properties = {key: value for key, value in properties.items() if value}
        return properties
