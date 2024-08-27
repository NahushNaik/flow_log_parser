import logging
from typing import DefaultDict
from . import PortProtocol


class OutputWriter:
    """
    Writes the results of the flow log processing to output files.

    The OutputWriter class is responsible for writing the counts of tags and
    port/protocol combinations to separate output files.

    Attributes:
    ----------
        output_file : str
            Path of the output file provided from the command line arguments.
    """

    def __init__(self, output_file: str):
        self.output_file = output_file

    def write(self, tag_counts: DefaultDict[str, int], combination_counts: DefaultDict[PortProtocol, int]) -> None:
        """
        Writes the counts to the output file.
        """
        try:
            with open(self.output_file, mode='w') as file:
                file.write("Tag Counts:\n")
                file.write("Tag\t\tCount\n")
                for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
                    file.write(f"{tag}\t\t{count}\n")

                file.write("\nPort/Protocol Combination Counts:\n")
                file.write("Port\tProtocol\tCount\n")
                for (dstport, protocol), count in sorted(combination_counts.items()):
                    file.write(f"{dstport}\t{protocol}\t{count}\n")
        except IOError:
            logging.error(f"Error: Could not write to the file '{self.output_file}'.")
            raise
