import argparse
import pandas as pd
from .data_loader import DataLoader
from .api_fetcher import APIFetcher
from .data_merger import DataMerger

def load_data():
    static_data_loader = DataLoader('data/HDBCarparkInformation.csv')
    static_data = static_data_loader.load_data()

    api_fetcher = APIFetcher('https://api.data.gov.sg/v1/transport/carpark-availability')
    real_time_data = api_fetcher.fetch_data()
    
    if 'carpark_number' in real_time_data.columns and 'car_park_no' not in real_time_data.columns:
        real_time_data.rename(columns={'carpark_number': 'car_park_no'}, inplace=True)

    data_merger = DataMerger()
    merged_data = data_merger.merge_data(static_data, real_time_data)
    return merged_data

def query_carpark(carpark_number, data):
    """ Query car park details by car park number. """
    result = data[data['car_park_no'] == carpark_number]
    if result.empty:
        print("No data found for the specified car park number.")
    else:
        row = result.iloc[0]
        print("Car Park Details:")
        print(f"Car Park No: {row['car_park_no']}")
        print(f"Address: {row['address']}")
        print(f"Operating Hours: {row.get('operating_hours', 'N/A')}")
        print(f"Rules: {row.get('rules', 'N/A')}")
        print(f"Parking System: {row.get('type_of_parking_system', 'N/A')}")
        print(f"Capacity: Total lots: {row.get('total_lots', 'N/A')}, Lots available: {row.get('lots_available', 'N/A')}")
        print(f"Coordinates: (x: {row.get('x_coord', 'N/A')}, y: {row.get('y_coord', 'N/A')})")
        print(f"Update Time: {row.get('update_datetime', 'N/A')}")
        print(f"Feed Timestamp: {row.get('feed_timestamp', 'N/A')}")

def search_by_address(address, data):
    """ Search car parks by address. """
    result = data[data['address'].str.contains(address, case=False, na=False)]
    if result.empty:
        print("No data found for the specified address.")
    else:
        for _, row in result.iterrows():
            print("Car Park Details:")
            print(f"Car Park No: {row['car_park_no']}")
            print(f"Address: {row['address']}")
            print(f"Operating Hours: {row.get('operating_hours', 'N/A')}")
            print(f"Rules: {row.get('rules', 'N/A')}")
            print(f"Parking System: {row.get('type_of_parking_system', 'N/A')}")
            print(f"Capacity: Total lots: {row.get('total_lots', 'N/A')}, Lots available: {row.get('lots_available', 'N/A')}")
            print(f"Coordinates: (x: {row.get('x_coord', 'N/A')}, y: {row.get('y_coord', 'N/A')})")
            print(f"Update Time: {row.get('update_datetime', 'N/A')}")
            print(f"Feed Timestamp: {row.get('feed_timestamp', 'N/A')}")
            print("-------------------------------------------------")

def view_last_update(carpark_number, data):
    """ View the last update time for a specific car park. """
    result = data[data['car_park_no'] == carpark_number]
    if result.empty:
        print("No data found for the specified car park number.")
    else:
        print(f"Last Update Time: {result['update_datetime'].iloc[0]}")

def main():
    parser = argparse.ArgumentParser(description="Car Park App CLI")
    parser.add_argument('--query', help='Query car park details by car park number.')
    parser.add_argument('--search', help='Search car parks by address.')
    parser.add_argument('--view', help='View last update time of a car park.')
    args = parser.parse_args()

    data = load_data()

    if args.query:
        query_carpark(args.query, data)
    elif args.search:
        search_by_address(args.search, data)
    elif args.view:
        view_last_update(args.view, data)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
