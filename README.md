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
For example: 

```bash
python main.py --query ACM
```
### Searching by address

```bash
python main.py --search <address>
```
For example: 

```bash
python main.py --search "ALJUNIED"
```

### View last updated time

```bash
python main.py --view <carpark_number>
```
For example: 

```bash
python main.py --view ACM
```

### Testing

Unit tests are in the `tests/` directory. It covers data loading, processing, and analysis.

Run all tests using:

```bash
python -m unittest discover -s tests
```
## Key Design Decisions

- **Modular Structure**: The project is divided into distinct modules—DataLoader, APIFetcher, DataMerger, and CLI—to isolate responsibilities. This improves maintainability and makes each component easier to test.
- **Error Handling**: Each module includes error handling for specific issues (e.g., file not found, JSON parsing errors, missing columns) so that problems are detected and reported at the earliest stage.
- **Missing Values**: The system is designed to handle missing or invalid data gracefully, using default values (like "N/A") where appropriate.
- **Data Handling:**: Merging static CSV data with real-time API data is performed via a common key (car park number), ensuring consistency in the final dataset.
- **Comprehensive Testing**: Separate testing strategy with mocks was implemented to ensure module reliability.
- **Command-Line Interface (CLI):**: The CLI is built with clear optional arguments (--query, --search, --view) to allow users to easily access information. The CLI displays merged information from both static and real-time sources in a clear format that meets the project requirements.

## Assumptions Made

- **Merge Key Consistency:**: It is assumed that the common merge key is car_park_no in the static CSV and carpark_number in the API data. The project automatically renames the API column to ensure consistency.
- **Real-Time API Structure:**: The API endpoint is assumed to return data in a known JSON structure. Each response contains an "items" list with a global "timestamp" and a "carpark_data" list. Each car park record in "carpark_data" includes keys such as carpark_number, update_datetime, and a nested "carpark_info" list with total_lots, lot_type, and lots_available.
- **CLI Behavior:**: The CLI is designed to accept optional arguments for querying by car park number, searching by address, or viewing the last update time. It is assumed that users will only use these options. 

## System Architecture

```
car_park_status/
├── data/
│   └── HDBCarparkInformation.csv 
├── modules/
│   ├── __init__.py               
│   ├── data_loader.py            
│   ├── api_fetcher.py            
│   ├── data_merger.py            
│   └── cli.py                  
├── tests/
│   ├── __init__.py               
│   ├── test_data_loader.py       
│   ├── test_api_fetcher.py       
│   ├── test_data_merger.py       
│   └── test_cli.py              
├── .gitignore                    
├── main.py                       
├── requirements.txt              
└── README.md                    
```

## Dependencies

Dependencies are listed in the `requirements.txt` file and include:

- pandas
- openpyxl (for Excel file handling)

## Further Improvements

This application could be further improved to be deployed in the cloud. To do so this application could be deployed as a containerized application using Docker, which encapsulates python code handling data loading, restaurant details extraction, event processing, and ratings analysis into a consistent, reproducible environment. 

The Docker image would be built from a Dockerfile that installs dependencies from the requirements.txt file and sets the entry point to the main analysis pipeline. This container can then be deployed to AWS or any other platforms

Input data (the JSON and Excel files) can reside in a cloud object storage service separating the storage from compute and ensuring data durability. After processing, output CSV files would be uploaded back to this storage for further analysis. 
