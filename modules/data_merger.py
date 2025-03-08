import pandas as pd

class DataMerger:
    def __init__(self):
        pass

    def merge_data(self, static_data, real_time_data):
        if 'car_park_no' not in static_data.columns or 'car_park_no' not in real_time_data.columns:
            raise ValueError("Missing necessary car park number columns in datasets.")

        if not static_data['car_park_no'].apply(lambda x: isinstance(x, str)).all():
            raise ValueError("Invalid format in merge key 'car_park_no'.")

        merged_data = pd.merge(static_data, real_time_data, on='car_park_no', how='left')
        merged_data.fillna({'lots_available': 0}, inplace=True)
        return merged_data

    def validate_data(self, df):
        essential_columns = {'car_park_no', 'address', 'total_lots', 'lots_available'}
        missing_columns = essential_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing essential columns: {missing_columns}")

    def handle_missing_data(self, df):
        df.fillna({'lots_available': 0}, inplace=True)
        return df
