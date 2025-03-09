import os
import requests
import json
import time
from tqdm import tqdm  # Progress bar for visualization

# Define API base URL
BASE_URL = "https://aa.usno.navy.mil/api/rstt/oneday"

# Define the range of years
START_YEAR = 1700
END_YEAR = 1799

# Define output directory
OUTPUT_DIR = "../data/raw/"

# Create directory if it does not exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define U.S. state capitals, coordinates, and time zones
state_data = {
    "Alabama": (32.3770, -86.3006, -6),
    "Alaska": (58.3019, -134.4197, -9),
    "Arizona": (33.4484, -112.0740, -7),
    "Arkansas": (34.7465, -92.2896, -6),
    "California": (38.575764, -121.478851, -8),
    "Colorado": (39.7392, -104.9903, -7),
    "Connecticut": (41.7640, -72.6822, -5),
    "Delaware": (39.1582, -75.5244, -5),
    "Florida": (30.4383, -84.2807, -5),
    "Georgia": (33.7490, -84.3880, -5),
    "Hawaii": (21.3070, -157.8584, -10),
    "Idaho": (43.6178, -116.1997, -7),
    "Illinois": (39.7980, -89.6440, -6),
    "Indiana": (39.7684, -86.1581, -5),
    "Iowa": (41.5908, -93.6208, -6),
    "Kansas": (39.0473, -95.6752, -6),
    "Kentucky": (38.1868, -84.8753, -5),
    "Louisiana": (30.4571, -91.1874, -6),
    "Maine": (44.3070, -69.7817, -5),
    "Maryland": (38.9784, -76.4922, -5),
    "Massachusetts": (42.3601, -71.0589, -5),
    "Michigan": (42.7335, -84.5555, -5),
    "Minnesota": (44.9551, -93.1022, -6),
    "Mississippi": (32.2988, -90.1848, -6),
    "Missouri": (38.5767, -92.1735, -6),
    "Montana": (46.5891, -112.0391, -7),
    "Nebraska": (40.8081, -96.6997, -6),
    "Nevada": (39.1638, -119.7664, -8),
    "New Hampshire": (43.2081, -71.5376, -5),
    "New Jersey": (40.2206, -74.7691, -5),
    "New Mexico": (35.6822, -105.9394, -7),
    "New York": (42.6526, -73.7562, -5),
    "North Carolina": (35.7804, -78.6391, -5),
    "North Dakota": (46.8208, -100.7837, -6),
    "Ohio": (39.9612, -82.9988, -5),
    "Oklahoma": (35.4676, -97.5164, -6),
    "Oregon": (44.9429, -123.0351, -8),
    "Pennsylvania": (40.2732, -76.8867, -5),
    "Rhode Island": (41.8236, -71.4222, -5),
    "South Carolina": (34.0007, -81.0348, -5),
    "South Dakota": (44.3668, -100.3538, -6),
    "Tennessee": (36.1627, -86.7816, -6),
    "Texas": (30.2672, -97.7431, -6),
    "Utah": (40.7608, -111.8910, -7),
    "Vermont": (44.2624, -72.5800, -5),
    "Virginia": (37.5407, -77.4360, -5),
    "Washington": (47.0379, -122.9007, -8),
    "West Virginia": (38.3498, -81.6326, -5),
    "Wisconsin": (43.0731, -89.4012, -6),
    "Wyoming": (41.1399, -104.8202, -7)
}

# Loop through years and states
for year in tqdm(range(START_YEAR, END_YEAR + 1), desc="Fetching Data by Year"):
    yearly_data = []  # Store all states' data for the given year

    for state, (lat, lon, tz) in state_data.items():
        date = f"{year}-06-21"  # June 21st (Summer Solstice) as reference

        params = {
            "date": date,
            "coords": f"{lat},{lon}",
            "tz": str(tz),  # Use the correct time zone for each state
            "dst": "true"
        }

        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                result = response.json()

                if "properties" in result and "data" in result["properties"]:
                    sun_moon_data = result["properties"]["data"]
                    yearly_data.append({
                        "Year": year,
                        "State": state,
                        "Latitude": lat,
                        "Longitude": lon,
                        "Sun and Moon Data": sun_moon_data
                    })
                    print(f"Data retrieved for {state} in {year}")
                else:
                    print(f"No data found for {state} in {year}")
            else:
                print(f"Failed to fetch data for {state} in {year}")

        except Exception as e:
            print(f"Error retrieving data for {state} in {year}: {e}")

        time.sleep(1)  # Reduce server overload

    # Save data for the year as a separate JSON file
    file_path = os.path.join(OUTPUT_DIR, f"sun_moon_{year}.json")
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(yearly_data, json_file, indent=4)

print("Data collection complete! JSON files saved in '../data/raw/'")
