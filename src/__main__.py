"""
MCO ETL.
"""
# standard
import json
import logging
import time

# third party
import owlready2
import datetime

# local
from libs import arguments
from libs import file_manager
from regulondb import ontologies, terms


def run(**kwargs):
    """
    Run function, controls program functions and generates output files.

    Args:
        kwargs (dict): Dictionary of arguments
        kwargs.input_file: String, The path to the input file.
        kwargs.output_dirs_path: String, The path to the output directory where results will be stored.
        kwargs.collection_name: String, The name of the collection to be processed.
        kwargs.url: String, The URL of the resource to be used.
    """

    if kwargs.get('url', None):
        owl_url = kwargs.get('url', '')
        print("Loading ontology from url: : ", owl_url)
        logging.info("Loading ontology from url: " + owl_url)
        ontology_owl_obj = owlready2.get_ontology(owl_url).load()

    elif kwargs.get('input_file', None):
        file_manager.validate_file_path(kwargs.get('input_file'))
        owl_file = kwargs.get('input_file', '')
        print("Loading ontology from file: ", owl_file.split("/")[-1])
        logging.info("Loading ontology from file: " + owl_file)
        ontology_owl_obj = owlready2.get_ontology(owl_file).load()
    else:
        raise ValueError("Please provide an input ontology url or input file name.")

    if ontology_owl_obj:
        print("MCO loaded successfully")
        logging.info("MCO loaded successfully")

        print("Setting up Ontologies' process")
        logging.info("Setting up Ontologies' process")
        ontology_obj = ontologies.get_regulondb_ontologies(
            only_properties_with_values=True,
            ontology_owl_obj=ontology_owl_obj
        )
        ontology_dict = {
            "classAcronym": "ONTOL",
            "subClassAcronym": ontology_obj.get("ontologyCode"),
            "collectionName": "ontologies",
            "ontologyName": "microbialConditionOntology",
            "collectionData": [ontology_obj],
        }
        file_manager.create_json(filename='ontology', objects=ontology_dict, output=kwargs.get('output_dirs_path'))

        print("Setting up Terms' process")
        logging.info("Setting up Terms' process")
        terms_objs = terms.get_regulondb_terms(
            only_properties_with_values=True,
            ontology_owl_obj=ontology_owl_obj,
            ontology_code=ontology_obj.get("ontologyCode"),
            base_iri=ontology_owl_obj.base_iri
        )
        terms_dict = {
            "classAcronym": "ONTOL",
            "subClassAcronym": ontology_obj.get("ontologyCode"),
            "collectionName": "terms",
            "ontologyName": "microbialConditionOntology",
            "collectionData": terms_objs,
        }
        file_manager.create_json(filename='terms', objects=terms_dict, output=kwargs.get('output_dirs_path'))
    else:
        raise ValueError("MCO failed to load :(, please check the input ontology url or input file name. :)")


if __name__ == '__main__':
    """
    Main function RegulonDB HT ETL.
    Initializes variables for program execution.
    """

    args = arguments.load_arguments()

    file_manager.set_log(args.log, args.collection_name, datetime.date.today())

    file_manager.validate_directories(args.output_path)
    output_dirs_path = args.output_path

    print("Initializing RegulonDB MCO ETL")
    logging.info(f'Initializing RegulonDB MCO ETL')

    input_file = args.input_file

    run(
        input_file=input_file,
        output_dirs_path=output_dirs_path,
        collection_name=args.collection_name,
        url=args.url,
    )
