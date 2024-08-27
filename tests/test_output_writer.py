import unittest
from application import output_writer, PortProtocol
from unittest.mock import patch, mock_open
from collections import defaultdict


class TestOutputWriter(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_write_output_success(self, mock_file):
        writer = output_writer.OutputWriter(mock_file)
        # Prepare test data
        tag_counts = defaultdict(int, {'sv_p1': 1, 'sv_p2': 1})
        combination_counts = defaultdict(int, {
            PortProtocol(25, 'tcp'): 1,
            PortProtocol(68, 'udp'): 1
        })

        # Test writing the output
        writer.write(tag_counts, combination_counts)

        # Assert that the correct data was written to the file
        mock_file().write.assert_any_call("Tag Counts:\n")
        mock_file().write.assert_any_call("Tag\t\tCount\n")
        mock_file().write.assert_any_call("sv_p1\t\t1\n")
        mock_file().write.assert_any_call("\nPort/Protocol Combination Counts:\n")
        mock_file().write.assert_any_call("Port\tProtocol\tCount\n")
        mock_file().write.assert_any_call("25\ttcp\t1\n")

    @patch('builtins.open', side_effect=IOError)
    def test_output_writer_io_error(self, mock_file):
        # Prepare test data
        tag_counts = defaultdict(int, {'sv_p1': 1, 'sv_p2': 1})
        combination_counts = defaultdict(int, {
            PortProtocol(25, 'tcp'): 1,
            PortProtocol(68, 'udp'): 1
        })

        # Test writing the output
        writer = output_writer.OutputWriter(mock_file)

        # Assert that the error is raised
        with self.assertRaises(IOError):
            writer.write(tag_counts, combination_counts)


if __name__ == '__main__':
    unittest.main()
