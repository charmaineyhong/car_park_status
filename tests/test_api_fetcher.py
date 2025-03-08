import unittest
from unittest.mock import patch
import requests
import pandas as pd
from modules.api_fetcher import APIFetcher

class TestAPIFetcher(unittest.TestCase):
    def setUp(self):
        self.api_url = 'https://api.example.com/hdb_carpark_availability'
        self.fetcher = APIFetcher(self.api_url)

    @patch('requests.get')
    def test_fetch_data_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "timestamp": "2025-03-08T23:16:36+08:00",
                    "carpark_data": [
                        {
                            "carpark_number": "A11",
                            "update_datetime": "2025-03-08T23:16:32",
                            "carpark_info": [
                                {
                                    "total_lots": "410",
                                    "lot_type": "C",
                                    "lots_available": "236"
                                }
                            ]
                        },
                        {
                            "carpark_number": "TR1",
                            "update_datetime": "2025-03-08T23:15:05",
                            "carpark_info": [
                                {
                                    "total_lots": "391",
                                    "lot_type": "C",
                                    "lots_available": "143"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        expected_df = pd.DataFrame({
            "carpark_number": ["A11", "TR1"],
            "update_datetime": ["2025-03-08T23:16:32", "2025-03-08T23:15:05"],
            "total_lots": [410, 391],
            "lot_type": ["C", "C"],
            "lots_available": [236, 143],
            "feed_timestamp": ["2025-03-08T23:16:36+08:00", "2025-03-08T23:16:36+08:00"]
        })
        result_df = self.fetcher.fetch_data()
        pd.testing.assert_frame_equal(result_df, expected_df)

    @patch('requests.get')
    def test_fetch_data_http_error(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Error 404: Not Found")
        with self.assertRaises(requests.exceptions.HTTPError):
            self.fetcher.fetch_data()

    @patch('requests.get')
    def test_fetch_data_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.fetcher.fetch_data()

    @patch('requests.get')
    def test_fetch_data_invalid_json(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")
        with self.assertRaises(ValueError):
            self.fetcher.fetch_data()

    @patch('requests.get')
    def test_fetch_data_incomplete_data(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status = unittest.mock.Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "timestamp": "2025-03-08T23:16:36+08:00",
                    "carpark_data": [
                        {
                            "carpark_number": "A11",
                            "update_datetime": "2025-03-08T23:16:32",
                            "carpark_info": [] 
                        }
                    ]
                }
            ]
        }
        with self.assertRaises(ValueError):
            self.fetcher.fetch_data()

if __name__ == '__main__':
    unittest.main()
