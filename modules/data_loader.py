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
        return data

    def validate_data(self, data):
        required_columns = {'carpark_number', 'update_datetime', 'total_lots', 'lot_type', 'lots_available'}
        if not required_columns.issubset(data.columns):
            missing = required_columns - set(data.columns)
            raise ValueError(f"Missing required columns: {missing}")
        
        if data['total_lots'].dtype != 'int' or data['total_lots'].min() < 0:
            raise ValueError("Total lots must be a non-negative integer.")
        
        if data['lots_available'].dtype != 'int' or data['lots_available'].min() < 0:
            raise ValueError("Lots available must be a non-negative integer.")

if __name__ == "__main__":
    loader = DataLoader('data/HDBCarparkInformation.csv')
    try:
        carpark_data = loader.load_data()
        print(carpark_data.head())
    except Exception as e:
        print(e)
