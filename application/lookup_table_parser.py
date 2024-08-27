import csv
import logging
from typing import Dict
from . import PortProtocol

logging.basicConfig(level=logging.INFO)


class LookupTableParser:
    """
    Parses the lookup table from a CSV file.

    The lookup table contains mappings from (dstport, protocol) combinations
    to tags. This class reads the lookup table file and stores the mappings
    in a dictionary for quick lookup.

    Attributes:
    ----------
        lookup_file : str
            The path of the lookup_file passed from the command line arguments.
    """

    def __init__(self, lookup_file: str):
        self.lookup_file = lookup_file

    def parse(self) -> Dict[PortProtocol, str]:
        """
        Parses the lookup table CSV file.

        Returns:
            A dictionary mapping (dstport, protocol) to a tag.
        """
        lookup_table = {}
        try:
            with open(self.lookup_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    try:
                        dstport, protocol, tag = row
                        lookup_table[PortProtocol(int(dstport), protocol.lower())] = tag.strip().lower()
                    except ValueError:
                        logging.warning(f"Skipping malformed row in lookup table: {row}")
        except FileNotFoundError:
            logging.error(f"Error: The file '{self.lookup_file}' was not found.")
            raise
        except IOError:
            logging.error(f"Error: Could not read the file '{self.lookup_file}'.")
            raise

        return lookup_table
