import unittest
from unittest.mock import patch
from collections import defaultdict
from application import flow_log_processor, lookup_table_parser, output_writer, PortProtocol
from application.app import Application


class ApplicationTest(unittest.TestCase):

    @patch.object(lookup_table_parser.LookupTableParser, 'parse')
    @patch.object(flow_log_processor.FlowLogProcessor, 'process')
    @patch.object(output_writer.OutputWriter, 'write')
    def test_application_success(self, mock_write, mock_process, mock_parse):
        # Prepare mock data
        lookup_table = {
            PortProtocol(25, 'tcp'): 'sv_p1',
            PortProtocol(443, 'tcp'): 'sv_p2'
        }
        tag_counts = defaultdict(int, {'sv_p1': 1, 'sv_p2': 1})
        combination_counts = defaultdict(int, {
            PortProtocol(25, 'tcp'): 1,
            PortProtocol(443, 'tcp'): 1
        })

        # Set up mock methods
        mock_parse.return_value = lookup_table
        mock_process.return_value = (tag_counts, combination_counts)

        # Initialize the Application class
        app = Application('lookup_table.csv', 'flow_log.txt', 'output.txt')

        # Run the application
        app.run()

        # Assert that methods were called with expected arguments
        mock_parse.assert_called_once()
        mock_process.assert_called_once()
        mock_write.assert_called_once_with(tag_counts, combination_counts)


if __name__ == '__main__':
    unittest.main()
