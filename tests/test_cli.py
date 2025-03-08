import unittest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import argparse
from modules import cli

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.sample_merged_data = pd.DataFrame({
            'car_park_no': ['ACB', 'ACM', 'AH1'],
            'address': ['Location A', 'Location B', 'Location C'],
            'total_lots': [100, 150, 200],
            'lots_available': [50, 100, 150],
            'update_datetime': ['2025-03-08T23:16:32', '2025-03-08T23:16:17', '2025-03-08T23:16:32'],
            'x_coord': [1.0, 2.0, 3.0],
            'y_coord': [1.0, 2.0, 3.0],
            'type_of_parking_system': ['Electronic', 'Electronic', 'Coupon'],
            'operating_hours': ['24 Hours', '7 AM - 10 PM', '24 Hours'],
            'rules': ['No Restrictions', 'Night Parking Only', 'Permit Required']
        })

    @patch('modules.cli.argparse.ArgumentParser.parse_args')
    @patch('modules.cli.DataLoader')
    @patch('modules.cli.APIFetcher')
    @patch('modules.cli.DataMerger')
    def test_query_carpark(self, MockMerger, MockFetcher, MockLoader, mock_args):
        MockLoader.return_value.load_data.return_value = MagicMock()
        MockFetcher.return_value.fetch_data.return_value = MagicMock()
        MockMerger.return_value.merge_data.return_value = self.sample_merged_data
        # Simulate CLI arguments for querying car park "ACB"
        mock_args.return_value = argparse.Namespace(query='ACB', search=None, view=None)

        with patch('builtins.print') as mocked_print:
            cli.main()
            # Check that one of the print calls contains the expected car park number.
            self.assertTrue(any("Car Park No: ACB" in str(c) for c in mocked_print.call_args_list))
            # Check that "Feed Timestamp: N/A" is printed.
            self.assertTrue(any("Feed Timestamp: N/A" in str(c) for c in mocked_print.call_args_list))

    @patch('modules.cli.argparse.ArgumentParser.parse_args')
    @patch('modules.cli.DataLoader')
    @patch('modules.cli.APIFetcher')
    @patch('modules.cli.DataMerger')
    def test_search_by_address(self, MockMerger, MockFetcher, MockLoader, mock_args):
        MockLoader.return_value.load_data.return_value = MagicMock()
        MockFetcher.return_value.fetch_data.return_value = MagicMock()
        MockMerger.return_value.merge_data.return_value = self.sample_merged_data
        # Simulate CLI arguments for searching by address "Location B"
        mock_args.return_value = argparse.Namespace(query=None, search='Location B', view=None)

        with patch('builtins.print') as mocked_print:
            cli.main()
            printed_calls = mocked_print.call_args_list
            self.assertTrue(any("Address: Location B" in str(c) for c in printed_calls))
            self.assertTrue(any("-------------------------------------------------" in str(c) for c in printed_calls))

    @patch('modules.cli.argparse.ArgumentParser.parse_args')
    @patch('modules.cli.DataLoader')
    @patch('modules.cli.APIFetcher')
    @patch('modules.cli.DataMerger')
    def test_view_last_update(self, MockMerger, MockFetcher, MockLoader, mock_args):
        MockLoader.return_value.load_data.return_value = MagicMock()
        MockFetcher.return_value.fetch_data.return_value = MagicMock()
        MockMerger.return_value.merge_data.return_value = self.sample_merged_data
        # Simulate CLI arguments for viewing last update for "ACB"
        mock_args.return_value = argparse.Namespace(query=None, search=None, view='ACB')

        with patch('builtins.print') as mocked_print:
            cli.main()
            mocked_print.assert_any_call("Last Update Time: 2025-03-08T23:16:32")

    @patch('modules.cli.argparse.ArgumentParser.parse_args')
    @patch('modules.cli.DataLoader')
    @patch('modules.cli.APIFetcher')
    @patch('modules.cli.DataMerger')
    def test_missing_required_fields(self, MockMerger, MockFetcher, MockLoader, mock_args):
        # Create a sample merged DataFrame missing a required field ('address').
        incomplete_data = pd.DataFrame({
            'car_park_no': ['ACB'],
            # 'address' column is missing!
            'total_lots': [100],
            'lots_available': [50],
            'update_datetime': ['2025-03-08T23:16:32'],
            'x_coord': [1.0],
            'y_coord': [1.0],
            'type_of_parking_system': ['Electronic'],
            'operating_hours': ['24 Hours'],
            'rules': ['No Restrictions']
        })
        MockLoader.return_value.load_data.return_value = MagicMock()
        MockFetcher.return_value.fetch_data.return_value = MagicMock()
        MockMerger.return_value.merge_data.return_value = incomplete_data
        mock_args.return_value = argparse.Namespace(query='ACB', search=None, view=None)
        
        with self.assertRaises(KeyError):
            cli.main()

    @patch('modules.cli.argparse.ArgumentParser.parse_args')
    @patch('modules.cli.DataLoader')
    @patch('modules.cli.APIFetcher')
    @patch('modules.cli.DataMerger')
    def test_invalid_numeric_field_format(self, MockMerger, MockFetcher, MockLoader, mock_args):
        invalid_data = pd.DataFrame({
            'car_park_no': ['ACB'],
            'address': ['Location A'],
            'total_lots': ['one hundred'],  
            'lots_available': [50],
            'update_datetime': ['2025-03-08T23:16:32'],
            'x_coord': [1.0],
            'y_coord': [1.0],
            'type_of_parking_system': ['Electronic'],
            'operating_hours': ['24 Hours'],
            'rules': ['No Restrictions']
        })
        MockLoader.return_value.load_data.return_value = MagicMock()
        MockFetcher.return_value.fetch_data.return_value = MagicMock()
        MockMerger.return_value.merge_data.return_value = invalid_data
        mock_args.return_value = argparse.Namespace(query='ACB', search=None, view=None)
        
        with patch('builtins.print') as mocked_print:
            cli.main()
            printed_calls = mocked_print.call_args_list
            self.assertTrue(any("Total lots: one hundred" in str(c) for c in printed_calls))

if __name__ == '__main__':
    unittest.main()
