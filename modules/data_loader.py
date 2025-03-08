import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        try:
            data = pd.read_csv(self.file_path)
            data = self.clean_data(data)
            self.validate_data(data)
            return data
        except FileNotFoundError:
            print(f"Error: The file at {self.file_path} was not found.")
            raise
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
            raise
        except pd.errors.ParserError:
            print("Error: There was an issue parsing the file.")
            raise

    def clean_data(self, data):
        data.columns = data.columns.str.strip()
        data.replace("", pd.NA, inplace=True)

        for col in data.select_dtypes(include=['object']).columns:
            data[col] = data[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
        data = data.where(pd.notnull(data), pd.NA)
        try:
            data['x_coord'] = data['x_coord'].astype(float)
            data['y_coord'] = data['y_coord'].astype(float)
            data['car_park_decks'] = data['car_park_decks'].astype(int)
            data['gantry_height'] = data['gantry_height'].astype(float)
        except Exception as e:
            print("Error converting numeric fields:", e)
            raise
        return data

    def validate_data(self, data):
        required_columns = {
            'car_park_no', 'address', 'x_coord', 'y_coord', 'car_park_type',
            'type_of_parking_system', 'short_term_parking', 'free_parking',
            'night_parking', 'car_park_decks', 'gantry_height', 'car_park_basement'
        }
        if not required_columns.issubset(data.columns):
            missing = required_columns - set(data.columns)
            raise ValueError(f"Missing required columns: {missing}")
        
        if data['car_park_decks'].min() < 0:
            raise ValueError("Car park decks must be non-negative.")
        if data['gantry_height'].min() < 0:
            raise ValueError("Gantry height must be non-negative.")


if __name__ == "__main__":
    loader = DataLoader('data/HDBCarparkInformation.csv')
    try:
        carpark_data = loader.load_data()
        print(carpark_data.head())
    except Exception as e:
        print(e)
