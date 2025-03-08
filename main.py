import argparse
from modules.data_loader import DataLoader
from modules.api_fetcher import APIFetcher
from modules.data_merger import DataMerger
from modules import cli



def main():
    parser = argparse.ArgumentParser(description="Car Park Application")
    parser.add_argument("action", help="Action to perform", choices=['query', 'search', 'view'])
    parser.add_argument("--carpark_number", help="Specify the carpark number for query or view")
    parser.add_argument("--address", help="Specify the address to search car parks")
    args = parser.parse_args()

    data_loader = DataLoader("C:/Users/charm/Downloads/HDBCarparkInformation.csv")
    api_fetcher = APIFetcher('https://api.data.gov.sg/v1/transport/carpark-availability')

    static_data = data_loader.load_data()
    availability_data = api_fetcher.fetch_data()

    data_merger = DataMerger()
    merged_data = data_merger.merge_data(static_data, availability_data)

    cli = CLI(merged_data)

    if args.action == 'query' and args.carpark_number:
        cli.query_carpark(args.carpark_number)
    elif args.action == 'search' and args.address:
        cli.search_by_address(args.address)
    elif args.action == 'view' and args.carpark_number:
        cli.view_last_update(args.carpark_number)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli.main()



