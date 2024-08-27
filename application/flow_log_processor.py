import logging
from typing import Dict, DefaultDict, Tuple
from collections import defaultdict
from . import PortProtocol


class FlowLogProcessor:
    """
    Processes flow log data and generates reports based on a lookup table.

    The FlowLogProcessor class reads flow log data from a file, applies the tags
    from the lookup table, and counts occurrences of each tag and port/protocol
    combination.

    Attributes:
    ----------
        flow_log_file : str
            Path of the flow log file provided from the command line arguments.
        lookup_table : Dict[PortProtocol, str]
            The lookup_table object generated after the LookupTableParser is done with it's parsing.
    """

    def __init__(self, flow_log_file: str, lookup_table: Dict[PortProtocol, str]):
        self.flow_log_file = flow_log_file
        self.lookup_table = lookup_table

    def process(self) -> Tuple[DefaultDict[str, int], DefaultDict[PortProtocol, int]]:
        """
        Processes the flow log and counts tag occurrences and port/protocol combinations.
        Only port/protocol combinations that are tagged are included in the combination counts.

        Returns:
            Two dictionaries, one for tag counts and one for port/protocol combination counts.
        """
        tag_counts = defaultdict(int)
        combination_counts = defaultdict(int)

        tagged_combinations = {key for key, tag in self.lookup_table.items() if tag != 'untagged'}

        try:
            with open(self.flow_log_file, mode='r') as file:
                for line in file:
                    try:
                        dstport, protocol = line.strip().split()
                        key = PortProtocol(int(dstport), protocol.lower())

                        tag = self.lookup_table.get(key, 'untagged')

                        if tag != 'untagged' and key in tagged_combinations:
                            combination_counts[key] += 1

                        tag_counts[tag] += 1
                    except ValueError:
                        logging.warning(f"Skipping malformed line in flow log: {line.strip()}")
        except FileNotFoundError:
            logging.error(f"Error: The file '{self.flow_log_file}' was not found.")
            raise
        except IOError:
            logging.error(f"Error: Could not read the file '{self.flow_log_file}'.")
            raise

        return tag_counts, combination_counts
