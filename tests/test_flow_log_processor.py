import unittest
from unittest.mock import mock_open, patch
from collections import defaultdict
from application import flow_log_processor, PortProtocol


class TestFlowLogProcessor(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="25 tcp\n68 udp\n")
    def test_process_flow_log_success(self, mock_file):
        # Prepare a lookup table
        lookup_table = {
            PortProtocol(25, 'tcp'): 'sv_p1',
            PortProtocol(68, 'udp'): 'sv_p2'
        }
        processor = flow_log_processor.FlowLogProcessor(mock_file, lookup_table)
        # Test processing the flow log
        tag_counts, combination_counts = processor.process()

        # Expected results
        expected_tag_counts = defaultdict(int, {
            'sv_p1': 1,
            'sv_p2': 1
        })
        expected_combination_counts = defaultdict(int, {
            PortProtocol(25, 'tcp'): 1,
            PortProtocol(68, 'udp'): 1
        })

        self.assertEqual(tag_counts, expected_tag_counts)
        self.assertEqual(combination_counts, expected_combination_counts)

    @patch('builtins.open', new_callable=mock_open)
    def test_flow_log_processor_malformed_row_success(self, mocked_open):
        # Prepare the mock flow log content with a malformed row
        flow_log_content = "25 tcp\n80\n443 tcp\n"
        mocked_open.return_value.__enter__.return_value = flow_log_content.splitlines()

        # Prepare a mock lookup table
        lookup_table = {
            PortProtocol(25, 'tcp'): 'sv_P1',
            PortProtocol(443, 'tcp'): 'sv_P2'
        }

        # Initialize the FlowLogProcessor with the mock data
        processor = flow_log_processor.FlowLogProcessor('fake_flow_log.txt', lookup_table)

        # Capture logs
        with self.assertLogs(level='WARNING') as log:
            tag_counts, combination_counts = processor.process()

            # Check if the warning was logged for the malformed line
            self.assertTrue(any("Skipping malformed line in flow log: 80" in message for message in log.output))

        # Verify the resulting tag counts and combination counts
        expected_tag_counts = defaultdict(int, {'sv_P1': 1, 'sv_P2': 1})
        expected_combination_counts = defaultdict(int, {
            PortProtocol(25, 'tcp'): 1,
            PortProtocol(443, 'tcp'): 1
        })

        self.assertEqual(tag_counts, expected_tag_counts)
        self.assertEqual(combination_counts, expected_combination_counts)

    @patch('builtins.open', new_callable=mock_open)
    def test_flow_log_processor_file_not_found_failure(self, mocked_open):
        # Simulate a FileNotFoundError when attempting to open the file
        mocked_open.side_effect = FileNotFoundError

        # Prepare a mock lookup table
        lookup_table = {
            PortProtocol(25, 'tcp'): 'sv_P1',
            PortProtocol(443, 'tcp'): 'sv_P2'
        }

        # Initialize the FlowLogProcessor with the mock data
        processor = flow_log_processor.FlowLogProcessor('non_existent_file.txt', lookup_table)

        # Capture logs
        with self.assertLogs(level='ERROR') as log:
            with self.assertRaises(FileNotFoundError):
                processor.process()

            # Check if the correct error message was logged
            self.assertTrue(
                any("Error: The file 'non_existent_file.txt' was not found." in message for message in log.output))


if __name__ == '__main__':
    unittest.main()
