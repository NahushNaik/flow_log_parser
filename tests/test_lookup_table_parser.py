import unittest
from application import lookup_table_parser, PortProtocol
from unittest.mock import mock_open, patch


class TestLookupTableParser(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="dstport,protocol,tag\n25,tcp,sv_P1\n68,udp,sv_P2\n")
    def test_parse_lookup_table_success(self, mock_file):
        parser = lookup_table_parser.LookupTableParser(mock_file)
        # Test parsing the lookup table
        expected_result = {
            PortProtocol(25, 'tcp'): 'sv_p1',
            PortProtocol(68, 'udp'): 'sv_p2'
        }
        lookup_table = parser.parse()
        self.assertEqual(lookup_table, expected_result)

    @patch('builtins.open', new_callable=mock_open)
    def test_lookup_table_parser_malformed_row_success(self, mocked_open):
        # Prepare the mock lookup table content with a malformed row
        lookup_table_content = "dstport,protocol,tag\n25,tcp,sv_P1\n80\n443,tcp,sv_P2\n"
        mocked_open.return_value.__enter__.return_value = lookup_table_content.splitlines()

        # Initialize the LookupTableParser with the mock data
        parser = lookup_table_parser.LookupTableParser('fake_lookup_file.csv')

        lookup_table = parser.parse()

        # Verify the resulting lookup table
        expected_lookup_table = {
            PortProtocol(25, 'tcp'): 'sv_p1',
            PortProtocol(443, 'tcp'): 'sv_p2'
        }

        self.assertEqual(lookup_table, expected_lookup_table)

    @patch('builtins.open', new_callable=mock_open)
    def test_lookup_table_parser_file_not_found_failure(self, mocked_open):
        # Simulate a FileNotFoundError when attempting to open the file
        mocked_open.side_effect = FileNotFoundError

        # Initialize the LookupTableParser with a file that will not be found
        parser = lookup_table_parser.LookupTableParser('non_existent_file.csv')

        # Capture logs
        with self.assertLogs(level='ERROR') as log:
            with self.assertRaises(FileNotFoundError):
                parser.parse()

            # Check if the correct error message was logged
            self.assertTrue(
                any("Error: The file 'non_existent_file.csv' was not found." in message for message in log.output))

if __name__ == '__main__':
    unittest.main()
