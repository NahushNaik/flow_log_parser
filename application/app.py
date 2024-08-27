import argparse
from .lookup_table_parser import LookupTableParser
from .flow_log_processor import FlowLogProcessor
from .output_writer import OutputWriter


class Application:
    """
    The main application class that orchestrates the flow log processing.

    This class ties together the LookupTableParser, FlowLogProcessor, and OutputWriter
    to perform the complete operation of parsing flow logs, applying tags, and generating
    output files.

    Attributes:
    ----------
        lookup_file : str
            Path of the lookup file provided from the command line arguments.
        flow_log_file : str
            Path of the flow log file provided from the command line arguments.
        output_file : str
            Path of the output file provided from the command line arguments.
    """

    def __init__(self, lookup_file: str, flow_log_file: str, output_file: str):
        self.lookup_file = lookup_file
        self.flow_log_file = flow_log_file
        self.output_file = output_file

    def run(self):
        # Parse lookup table
        parser = LookupTableParser(self.lookup_file)
        lookup_table = parser.parse()

        # Process flow log
        processor = FlowLogProcessor(self.flow_log_file, lookup_table)
        tag_counts, combination_counts = processor.process()

        # Write output
        writer = OutputWriter(self.output_file)
        writer.write(tag_counts, combination_counts)


def main():
    parser = argparse.ArgumentParser(description='Process flow logs and generate output.')
    parser.add_argument('lookup_file', type=str, help='Path to the lookup table file.')
    parser.add_argument('flow_log_file', type=str, help='Path to the flow log file.')
    parser.add_argument('output_file', type=str, help='Path to the output file.')

    args = parser.parse_args()

    app = Application(args.lookup_file, args.flow_log_file, args.output_file)
    app.run()


if __name__ == "__main__":
    main()
