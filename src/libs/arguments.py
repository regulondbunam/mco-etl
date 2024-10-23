# standard
import argparse

# third party


# local


def get_arguments():
    """
    Defines the arguments that the program will support.

    Returns:
        arguments: argparse Object, defined arguments for the execution of the program.
    """

    # ARGUMENTS DESCRIPTION

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Extract and Transform data from .owl Ontology, and write data to JSON files",
        epilog="You need to provided at least one entity argument(--datasets, --tfbinding, etc...)")

    parser.add_argument(
        "-i",
        "--inputfile",
        dest="inputfile",
        help="Input Ontology file name"
    )

    parser.add_argument(
        "-o",
        "--outputfile",
        dest="outputfile",
        help="Output Ontology terms file name"
        )

    parser.add_argument(
        "-m",
        "--metadatafile",
        dest="metadatafile",
        help="Output Ontology metadata file name"
    )

    parser.add_argument(
        "-u",
        "--url",
        dest="url",
        help="Input Ontology source"
    )

    parser.add_argument(
        "-l",
        "--log",
        dest="log",
        help="Log file name"
    )

    parser.add_argument(
        "-s",
        "--schemaversion",
        dest="schemaversion",
        help="Schema Version"
    )

    arguments = parser.parse_args()
    return arguments


def load_arguments():
    """
    Load the arguments that the program will support.

    Returns:
        arguments: argparse Object, loaded arguments for the execution of the program.
    """

    arguments = get_arguments()
    return arguments
