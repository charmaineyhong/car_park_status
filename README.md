# Car Park Status Application

## Project Overview
This application is designed to assist users in finding real-time parking availability by merging static car park details with live data from HDB car parks. It is to provide a comprehensive view of car park availability and details.

## Data Sources
- **Static Car Park Information:** This data includes details such as car park location, type and more information which are provided in a CSV file format.
- **Carpark Availability API:** Real-time availability data for car parks is fetched from an API, which updates the status of parking spaces continuously throughout the day.

## Modules
This application consists of several modules, each handling a specific aspect of the application:

### 1. Data Loader (`data_loader.py`)
Loads and cleans the static car park details from the CSV file. It validates that all required fields (e.g., `car_park_no`, `address`, `x_coord`, `y_coord`, etc.) are present and converts numeric fields appropriately.

### 2. API Fetcher (`api_fetcher.py`)
Retrieves real-time car park availability data from the HDB API, processes the JSON response, and converts it into a structured Pandas DataFrame. It extracts key information such as `carpark_number`, `update_datetime`, `total_lots`, `lot_type`, `lots_available`, and the global feed timestamp.

### 3. Data Merger (`data_merger.py`)
Merges the static data with the API data based on a common key (`car_park_no`). If necessary, it renames columns so that both data sources use a consistent key. It also handles missing values to ensure data consistency.

### 4. Command Line Interface (`cli.py`)
Provides a command-line interface that allows users to:
  - Query car park details by car park number.
  - Search for car parks by address.
  - View the last update time for a car park.
  The CLI formats and displays merged data, including operating hours and rules, alongside static and real-time details.


## Running the Application

### For qureying by carpark number:

```bash
python main.py --query <insert carpark number>
```
###For example: 

```bash
python main.py --query ACM
```
### Searching by address

```bash
python main.py --search <address>
```
###For example: 

```bash
python main.py --search "ALJUNIED"
```

### View last updated time

```bash
python main.py --view <carpark_number>
```
###For example: 

```bash
python main.py --view ACM
```

### Testing

Unit tests are in the `tests/` directory. They cover data loading, processing, and analysis functionalities.

Run all tests using:

```bash
python -m unittest discover -s tests
```

## System Architecture

```
car_park_status/
├── data/
│   └── HDBCarparkInformation.csv        # Provided CSV file containing static car park details
├── modules/
│   ├── __init__.py               # Makes this directory a Python package
│   ├── data_loader.py            # Module to load and process CSV data
│   ├── api_fetcher.py            # Module to fetch real-time availability data from the API
│   ├── data_merger.py            # Module to merge CSV data and API data; includes validation/cleaning
│   └── cli.py                  # Module to handle command-line interface functionality
├── tests/
│   ├── __init__.py               # Makes this directory a Python package
│   ├── test_data_loader.py       # Unit tests for data_loader module
│   ├── test_api_fetcher.py       # Unit tests for api_fetcher module
│   ├── test_data_merger.py       # Unit tests for data_merger module
│   └── test_cli.py               # Unit tests for CLI functionality
├── .gitignore                    # Lists files/folders to ignore (e.g., __pycache__, venv/)
├── main.py                       # Entry point for the application (ties together modules and CLI)
├── requirements.txt              # Project dependencies (e.g., pandas, requests, argparse, etc.)
└── README.md                     # Documentation, including project overview, setup, and usage instructions
```


