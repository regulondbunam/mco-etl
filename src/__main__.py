#!/usr/bin/python
# -*- coding: UTF-8 -*-
from owlready2 import *
import json
import logging
import time
from mco_etl import arguments

# Default parameters
in_file = "mco-edt.owl"
in_url = ""
out_file = "mco_terms.json"
onto_file = "mco_ontology.json"
log_file = "mcoLog.log"
schema_version = 0.1
logger = logging.getLogger("LogDebug")

# Global variables
start_time = time.time()
args = arguments.load()


def loggingSetUp(logFileName):
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logFileName)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info("Initialized")


def genOutFile(onto):
    print("Generating")
    onto_meta = {}
    ontology_code = onto.metadata.NCIT_NHC0
    if ontology_code:
        ontology_code = onto.metadata.NCIT_NHC0[0]
    onto_meta["classAcronym"] = "ONTOL"
    onto_meta["subClassAcronym"] = ontology_code.upper()
    onto_meta["collectionName"] = "ontologies"
    onto_meta["ontologyName"] = "microbialConditionOntology"
    onto_meta["collectionData"] = []
    ver_iri = onto.metadata.versionInfo
    if ver_iri:
        ver_iri = ver_iri[0]
    onto_name = onto.metadata.label
    if onto_name:
        onto_name = onto_name[0]
    onto_creators = onto.metadata.contributor
    onto_notes = onto.metadata.IAO_0000116
    if onto_notes:
        onto_notes = onto_notes[0]
    onto_description = onto.metadata.description
    if onto_description:
        onto_description = onto_description[0]

    externalCrossReferences = []

    ecocyc_reference = {
        "externalCrossReferences_id": "|ECOCYC|",
        "objectId": onto.base_iri.replace("|", ""),
    }
    externalCrossReferences.append(ecocyc_reference)

    onto_properties = {
        "_id": onto.base_iri,  # Temporal ID,
        "citations": onto.imported_ontologies,
        "createdBy": onto_creators,
        "description": onto_description,
        "externalCrossReferences": externalCrossReferences,
        "iri": onto.base_iri,
        "name": onto_name,
        "note": onto_notes,
        "ontologyCode": ontology_code,
        "versionIri": f'{ver_iri}',
        "schemaVersion": schema_version,
    }
    onto_properties = {k: v for k, v in onto_properties.items() if v}
    onto_meta["collectionData"].append(onto_properties)
    with open(ontoFile, "w") as outfile:
        json.dump(onto_meta, outfile, indent=4)

    onto_classes = list(onto.classes())
    terms = {}
    terms["classAcronym"] = "ONTOL"
    terms["subClassAcronym"] = ontology_code.upper()
    terms["collectionName"] = "terms"
    terms["ontologyName"] = "microbialConditionOntology"
    terms["collectionData"] = []
    term_count = 0
    for onto_class in onto_classes:  # Terms iterator
        term_count += 1
        try:
            # obo ID from Url
            url_id = (onto_class.iri).split("/")[-1]
            url_id = url_id.replace("_", ":")

            # onto_class Label
            onto_class_label = onto_class.label
            if onto_class_label:
                onto_class_label = str(onto_class.label[0])
            # RegulonDB ID
            rdb_id = ontology_code + "|" + url_id + "|" + onto_class_label

            # Extract obo_name_space
            obo_name_space = onto_class.hasOBONamespace
            if obo_name_space:
                obo_name_space = obo_name_space[0]

            # Extract DbXref
            cross_ref = onto_class.hasDbXref

            # Extract parent classes
            sub_class_of_obj = onto_class.is_a
            sub_class_of_array = []
            for parent_obj in sub_class_of_obj:
                if str(parent_obj) == "owl.Thing":
                    # sub_class_of_array.append(str(parent_obj))
                    pass
                else:
                    if ".some(" not in str(parent_obj):
                        parent_label = parent_obj.label
                        parent_id = (parent_obj.iri).split("/")[-1]
                        parent_id = parent_id.replace("_", ":")
                        parent_id = ontology_code + "|" + \
                            parent_id + "|" + parent_label[0]
                        sub_class_of_array.append(parent_id)

            # Extract child classes
            sup_class_of_obj = list(onto_class.subclasses())
            sup_class_of_array = []
            for child_obj in sup_class_of_obj:
                if ".some(" not in str(child_obj):
                    child_label = child_obj.label
                    child_id = (child_obj.iri).split("/")[-1]
                    child_id = child_id.replace("_", ":")
                    child_id = ontology_code + "|" + \
                        child_id + "|" + child_label[0]
                    sup_class_of_array.append(child_id)

            # Description concat
            description = str(onto_class.description +
                              onto_class.MCO_0000382 + onto_class.IAO_0000112)
            description = description.replace("[", "")
            description = description.replace("]", "")

            # Definition concat
            definition = str(onto_class.definition +
                             onto_class.IAO_0000115 + onto_class.MCO_0000851)
            definition = definition.replace("[", "")
            definition = definition.replace("]", "")

            # Definition Source concat
            definitionSrc = onto_class.IAO_0000119
            if definitionSrc:
                definitionSrc = definitionSrc[0]

            # Author concat
            author = onto_class.createdBy + onto_class.created_by
            if author:
                author = author[0]

            # Creation Date concat
            creation_date = onto_class.creation_date
            if creation_date:
                creation_date = creation_date[0]

            externalCrossReferences = []

            ecocyc_reference = {
                "externalCrossReferences_id": "|ECOCYC|",
                "objectId": rdb_id,
            }
            externalCrossReferences.append(ecocyc_reference)

            term_type = []
            parents = []
            parents_list = list(onto_class.ancestors())
            for parent in parents_list:
                parents.append(f'{parent}')
            if 'zeco.ZECO_0000200' in parents:
                term_type.append('pH')
            if 'obo.NCIT_C14250' in parents:
                term_type.append('Organism')
            if 'obo.MCO_0000078' in parents:
                term_type.append('Aeration')
            if 'obo.PATO_0000146' in parents:
                term_type.append('Temperature')
            if 'obo.PATO_0001025' in parents:
                term_type.append('Pressure')
            if 'obo.MCO_0000077' in parents:
                term_type.append('Optical Density')
            if 'obo.MCO_0000342' in parents:
                term_type.append('Growth phase')
            if 'obo.OMP_0007156' in parents:
                term_type.append('Growth rate')
            if 'obo.MCO_0000883' in parents:
                term_type.append('Agitation speed')
            # TODO: Not verified
            if 'obo.MCO_0000383' in parents:
                term_type.append('Genetic Background')
            if 'obo.OBI_0000079' in parents:
                term_type.append('Medium')
                term_type.append('Medium Supplement')
            if 'obo.OBI_0000967' in parents:
                term_type.append('Vessel Type')

            terms_properties = {
                "_id": rdb_id,
                "contributors": {
                    "text": author,
                    "creationDate": creation_date,
                },
                "definition": {
                    "text": definition,
                    "source": definitionSrc,
                },
                "description": description,
                "externalCrossReferences": externalCrossReferences,
                "hasDbXRef": cross_ref,
                "hasOboNameSpace": obo_name_space,
                "hasRelatedSynonyms": onto_class.hasRelatedSynonym,
                "iri": onto_class.iri,
                "name": onto_class.label[0],
                "oboId": url_id,
                "ontologies_id": onto.base_iri,
                "subClassOf": sub_class_of_array,
                "superClassOf": sup_class_of_array,
                "synonyms": (onto_class.hasExactSynonym + onto_class.MCO_0000190),
                "schemaVersion": schema_version,
                # "termType": term_type
            }
            terms_properties["definition"] = {
                k: v for k, v in terms_properties["definition"].items() if v
            }
            terms_properties["contributors"] = {
                k: v for k, v in terms_properties["contributors"].items() if v
            }
            terms_properties = {k: v for k, v in terms_properties.items() if v}
            terms["collectionData"].append(terms_properties)
        except Exception:
            print("An exception occurred during generation")
            print(onto_class)
    with open(outFile, "w") as outfile:
        json.dump(terms, outfile, indent=4)
    print("Ready ", term_count, " terms readed")
    logger.info("Ready " + str(term_count) + " terms readed")
    print("Execution time: %s seconds" % (time.time() - start_time))
    logger.info("Execution time: %s seconds" % +(time.time() - start_time))
    exit()


if __name__ == '__main__':

    if args.log:
        logFile = args.log

    if args.schemaversion:
        schema_version = float(args.schemaversion)

    if args.metadatafile:
        ontoFile = args.metadatafile

    loggingSetUp(logFile)

    if args.url:
        inUrl = args.url
        print("Input ontology url: : ", inUrl)
        logger.info("Input ontology url: " + inUrl)
        if args.outputfile:
            outFile = args.outputfile
            print("Output file name: ", outFile)
            logger.info("Output file name: " + outFile)
            onto = get_ontology(inUrl).load()
            if onto:
                print("MCO loaded successfully")
                logger.info("MCO loaded successfully")
                genOutFile(onto)
        else:
            print("No output file!")
            logger.error("No output file!")
            exit()
    elif args.inputfile:
        inFile = args.inputfile
        print("Input file name: ", inFile)
        logger.info("Input file name: " + inFile)
        if args.outputfile:
            outFile = args.outputfile
            print("Output file name: ", outFile)
            logger.info("Output file name: " + outFile)
            onto = get_ontology("file://" + inFile).load()
            if onto:
                print("MCO loaded successfully")
                logger.info("MCO loaded successfully")
                genOutFile(onto)
        else:
            print("No output file!")
            logger.error("No output file!")
            exit()
    else:
        print("No input file!")
        logger.error("No intput file!")
