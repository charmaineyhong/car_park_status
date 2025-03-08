import unittest
import pandas as pd
from modules.data_merger import DataMerger

class TestDataMerger(unittest.TestCase):
    def setUp(self):
        self.merger = DataMerger()

        self.static_data = pd.DataFrame({
            'car_park_no': ['A', 'B', 'C'],
            'address': ['Location A', 'Location B', 'Location C'],
            'car_park_type': ['Basement', 'Surface', 'Multi-storey']
        })

        self.real_time_data = pd.DataFrame({
            'carpark_number': ['A', 'B', 'D'],
            'total_lots': [100, 200, 300],
            'lots_available': [50, 180, 0]
        })

    def test_merge_data_successful(self):
        self.real_time_data.rename(columns={'carpark_number': 'car_park_no'}, inplace=True)

        merged_df = self.merger.merge_data(self.static_data, self.real_time_data)

        self.assertTrue('total_lots' in merged_df.columns)
        self.assertEqual(len(merged_df), 3)  
        self.assertEqual(merged_df.at[2, 'lots_available'], 0)

    def test_data_validation_failure(self):
        with self.assertRaises(ValueError):
            self.merger.validate_data(self.static_data.drop(columns=['address']))

    def test_handle_missing_data(self):
        self.real_time_data.at[2, 'lots_available'] = pd.NA
        self.real_time_data.rename(columns={'carpark_number': 'car_park_no'}, inplace=True)

        merged_df = self.merger.merge_data(self.static_data, self.real_time_data)
        self.merger.handle_missing_data(merged_df)
        self.assertFalse(merged_df['lots_available'].isnull().any())

    def test_merge_with_non_matching_keys(self):
        self.real_time_data.rename(columns={'carpark_number': 'car_park_no'}, inplace=True)
        self.static_data.at[0, 'car_park_no'] = 'X'

        merged_df = self.merger.merge_data(self.static_data, self.real_time_data)

        self.assertTrue(pd.isna(merged_df.at[0, 'total_lots']))

    def test_invalid_format_handling(self):
        self.static_data.at[0, 'car_park_no'] = 123  
        self.real_time_data.rename(columns={'carpark_number': 'car_park_no'}, inplace=True)

        with self.assertRaises(ValueError):
            self.merger.merge_data(self.static_data, self.real_time_data)

if __name__ == '__main__':
    unittest.main()
