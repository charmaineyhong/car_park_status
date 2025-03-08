import requests
import pandas as pd

class APIFetcher:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise
        except ValueError as e:
            raise
        if "items" not in data or not data["items"]:
            raise ValueError("API response does not contain 'items' or it is empty.")

        item = data["items"][0]
        feed_timestamp = item.get("timestamp", None)
        carpark_data_list = item.get("carpark_data", [])

        records = []
        for record in carpark_data_list:
            carpark_number = record.get("carpark_number")
            update_datetime = record.get("update_datetime")
            carpark_info_list = record.get("carpark_info", [])
            if not carpark_number or not update_datetime or not carpark_info_list:
                continue
            info = carpark_info_list[0]
            try:
                total_lots = int(info.get("total_lots"))
                lot_type = info.get("lot_type")
                lots_available = int(info.get("lots_available"))
            except (ValueError, TypeError) as e:
                continue

            records.append({
                "carpark_number": carpark_number,
                "update_datetime": update_datetime,
                "total_lots": total_lots,
                "lot_type": lot_type,
                "lots_available": lots_available,
                "feed_timestamp": feed_timestamp
            })

        if not records:
            raise ValueError("No valid car park data found in API response.")

        return pd.DataFrame(records)

