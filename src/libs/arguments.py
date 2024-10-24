# standard
import argparse
from email.policy import default


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
        "--input-file",
        dest="input_file",
        help="Input Ontology file name"
    )

    parser.add_argument(
        "-o",
        "--output-path",
        dest="output_path",
        help="Output Ontology terms file name",
        metavar="../RawData/",
        default="../RawData/",
    )

    parser.add_argument(
        "-collection",
        "--collection-name",
        dest="collection_name",
        help="Collection name",
        default="terms",
        metavar="terms"
    )

    parser.add_argument(
        "-url",
        "--url",
        dest="url",
        help="Input Ontology source"
    )

    parser.add_argument(
        "-l",
        "--log",
        help="Path where the log of the process will be stored.",
        metavar="../logs/mco_etl_log/",
        default="../logs/mco_etl_log/",
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
