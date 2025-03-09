import os
import requests
import json
import time

def fetch_ncvs_data():
    """Fetches NCVS datasets from 1993 to 2023 and saves them to the data/raw directory."""
    # Define NCVS API Endpoints
    NCVS_API_ENDPOINTS = {
        "personal_victimization": "https://data.ojp.usdoj.gov/resource/gcuy-rt5g.json",
        "personal_population": "https://data.ojp.usdoj.gov/resource/r4j4-fdwx.json",
    }

    # Define the directory to save raw data
    data_dir = "../data/raw"
    os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists

    # Loop through each year from 1993 to 2023
    for year in range(1993, 2024):
        for dataset_name, url in NCVS_API_ENDPOINTS.items():
            try:
                print(f"Fetching {dataset_name} data for {year}...")

                # API parameters including year filter
                params = {
                    "$limit": 5000,  # Adjust if necessary (default API limit is 1,000)
                    "year": str(year)  # Filter data by year
                }

                response = requests.get(url, params=params)

                # Check if request was successful
                if response.status_code == 200:
                    data = response.json()  # Convert response to JSON

                    if data:  # Ensure there is data before saving
                        # Save JSON to file in data/raw directory
                        output_file = os.path.join(data_dir, f"ncvs_{dataset_name}_{year}.json")
                        with open(output_file, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=4)

                        print(f"Data for {year} saved as {output_file}")

                    else:
                        print(f"No data available for {dataset_name} in {year}")

                else:
                    print(f"Error fetching {dataset_name} for {year}: {response.status_code} - {response.text}")

                # Pause between requests to prevent rate limiting
                time.sleep(1)

            except Exception as e:
                print(f"Failed to fetch {dataset_name} for {year}: {e}")

    print("\nAll NCVS datasets retrieved successfully!")

if __name__ == "__main__":
    fetch_ncvs_data()