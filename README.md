# Car Park Status Application

## Project Overview
This application is designed to assist users in finding real-time parking availability by merging static car park details with live data from HDB car parks. It is to provide a comprehensive view of car park availability and details, enhancing user experience by offering accurate and timely information for better decision-making.

## Data Sources
- **Static Car Park Information:** This data includes details such as car park location, type, and number of lots, which are provided in a CSV file format.
- **Carpark Availability API:** Real-time availability data for car parks is fetched from an external API, which updates the status of parking spaces continuously throughout the day.

## Modules
This application consists of several modules, each handling a specific aspect of the application:

### 1. Data Loader (`data_loader.py`)
- **Purpose:** Loads and processes static car park details from a CSV file.
- **Functionality:** Reads data from CSV, performs initial data validation, and formats the data for further processing.

### 2. API Fetcher (`api_fetcher.py`)
- **Purpose:** Fetches real-time car park availability from the API.
- **Functionality:** Makes HTTP requests to the car park API, handles API responses, and formats the data for merging.

### 3. Data Merger (`data_merger.py`)
- **Purpose:** Merges static car park data with real-time availability data.
- **Functionality:** Combines data based on `carpark_number`, ensures consistency, and handles data validation and cleaning.

### 4. Command Line Interface (`cli.py`)
- **Purpose:** Provides a user interface for interacting with the application via the command line.
- **Functionality:** Supports commands to query by `carpark_number`, search by address, and view the last update time of the car park data.

## Running the Application

### For qureying by carpark number:

```bash
python main.py --query ACM
```

### Searching by address

```bash
python main.py --search "ALJUNIED"

```

### View last updated time

```bash
python main.py --view ACM
```

### To run unit tests

```bash
python -m unittest discover -s tests
```