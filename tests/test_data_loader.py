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
            'car_park_no': ['ACB', 'ACM'],
            'address': ['BLK 270/271 ALBERT CENTRE BASEMENT CAR PARK', 'BLK 98A ALJUNIED CRESCENT'],
            'x_coord': [30314.7936, 33758.4143],
            'y_coord': [31490.4942, 33695.5198],
            'car_park_type': ['BASEMENT CAR PARK', 'MULTI-STOREY CAR PARK'],
            'type_of_parking_system': ['ELECTRONIC PARKING', 'ELECTRONIC PARKING'],
            'short_term_parking': ['WHOLE DAY', 'WHOLE DAY'],
            'free_parking': ['NO', 'SUN & PH FR 7AM-10PM'],
            'night_parking': ['YES', 'YES'],
            'car_park_decks': [1, 5],
            'gantry_height': [1.80, 2.10],
            'car_park_basement': ['Y', 'N']
        })
        mock_read_csv.return_value = valid_data.copy()
        result = self.loader.load_data()
        pd.testing.assert_frame_equal(result, valid_data)

    @patch('pandas.read_csv')
    def test_load_data_with_cleaning(self, mock_read_csv):
        dirty_data = pd.DataFrame({
            'car_park_no ': [' ACB', 'ACM '],
            'address': [' BLK 270/271 ALBERT CENTRE BASEMENT CAR PARK ', 'BLK 98A ALJUNIED CRESCENT '],
            'x_coord': [30314.7936, 33758.4143],
            'y_coord': [31490.4942, 33695.5198],
            'car_park_type': [' BASEMENT CAR PARK', 'MULTI-STOREY CAR PARK '],
            'type_of_parking_system': [' ELECTRONIC PARKING', 'ELECTRONIC PARKING '],
            'short_term_parking': [' WHOLE DAY', 'WHOLE DAY '],
            'free_parking': [' NO', 'SUN & PH FR 7AM-10PM '],
            'night_parking': [' YES', 'YES '],
            'car_park_decks': [1, 5],
            'gantry_height': [1.80, 2.10],
            'car_park_basement': [' Y', 'N ']
        })
        cleaned_data = pd.DataFrame({
            'car_park_no': ['ACB', 'ACM'],
            'address': ['BLK 270/271 ALBERT CENTRE BASEMENT CAR PARK', 'BLK 98A ALJUNIED CRESCENT'],
            'x_coord': [30314.7936, 33758.4143],
            'y_coord': [31490.4942, 33695.5198],
            'car_park_type': ['BASEMENT CAR PARK', 'MULTI-STOREY CAR PARK'],
            'type_of_parking_system': ['ELECTRONIC PARKING', 'ELECTRONIC PARKING'],
            'short_term_parking': ['WHOLE DAY', 'WHOLE DAY'],
            'free_parking': ['NO', 'SUN & PH FR 7AM-10PM'],
            'night_parking': ['YES', 'YES'],
            'car_park_decks': [1, 5],
            'gantry_height': [1.80, 2.10],
            'car_park_basement': ['Y', 'N']
        })
        mock_read_csv.return_value = dirty_data.copy()
        result = self.loader.load_data()
        pd.testing.assert_frame_equal(result, cleaned_data)

    @patch('pandas.read_csv')
    def test_validate_data_failure_missing_columns(self, mock_read_csv):
        incomplete_data = pd.DataFrame({
            'car_park_no': ['ACB'],
            # 'address' is missing
            'x_coord': [30314.7936],
            'y_coord': [31490.4942],
            'car_park_type': ['BASEMENT CAR PARK'],
            'type_of_parking_system': ['ELECTRONIC PARKING'],
            'short_term_parking': ['WHOLE DAY'],
            'free_parking': ['NO'],
            'night_parking': ['YES'],
            'car_park_decks': [1],
            'gantry_height': [1.80],
            'car_park_basement': ['Y']
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
