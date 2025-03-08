import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from modules.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader('data/HDBCarparkInformation.csv')

    @patch('pandas.read_csv')
    def test_load_data_success(self, mock_read_csv):
        valid_data = pd.DataFrame({
            'carpark_number': ['A11', 'TR1'],
            'update_datetime': ['2025-03-08T23:16:25', '2025-03-08T23:15:05'],
            'total_lots': [410, 391],
            'lot_type': ['C', 'C'],
            'lots_available': [236, 143]
        })
        mock_read_csv.return_value = valid_data.copy()
        result = self.loader.load_data()
        pd.testing.assert_frame_equal(result, valid_data)

    @patch('pandas.read_csv')
    def test_load_data_with_cleaning(self, mock_read_csv):
        dirty_data = pd.DataFrame({
            'carpark_number ': [' A11', 'TR1 '],
            'update_datetime': [' 2025-03-08T23:16:25 ', '2025-03-08T23:15:05 '],
            'total_lots': [410, 391],
            'lot_type': [' C', 'C '],
            'lots_available': [236, 143]
        })
        cleaned_data = pd.DataFrame({
            'carpark_number': ['A11', 'TR1'],
            'update_datetime': ['2025-03-08T23:16:25', '2025-03-08T23:15:05'],
            'total_lots': [410, 391],
            'lot_type': ['C', 'C'],
            'lots_available': [236, 143]
        })
        mock_read_csv.return_value = dirty_data.copy()
        result = self.loader.load_data()
        pd.testing.assert_frame_equal(result, cleaned_data)

    @patch('pandas.read_csv')
    def test_validate_data_failure_missing_columns(self, mock_read_csv):
        incomplete_data = pd.DataFrame({
            'carpark_number': ['A11'],
            'update_datetime': ['2025-03-08T23:16:25'],
            'total_lots': [410]
        })
        mock_read_csv.return_value = incomplete_data.copy()
        with self.assertRaises(ValueError):
            self.loader.load_data()

    @patch('pandas.read_csv')
    def test_load_data_file_not_found(self, mock_read_csv):
        mock_read_csv.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.loader.load_data()

    @patch('pandas.read_csv')
    def test_load_data_empty_data_error(self, mock_read_csv):
        mock_read_csv.side_effect = pd.errors.EmptyDataError
        with self.assertRaises(pd.errors.EmptyDataError):
            self.loader.load_data()

    @patch('pandas.read_csv')
    def test_load_data_parser_error(self, mock_read_csv):
        mock_read_csv.side_effect = pd.errors.ParserError
        with self.assertRaises(pd.errors.ParserError):
            self.loader.load_data()

if __name__ == '__main__':
    unittest.main()
