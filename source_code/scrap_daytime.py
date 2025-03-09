import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Step 1: Define Paths
def define_paths():
    """
    Defines the relative paths for input and output files.

    Returns:
        dict: A dictionary containing paths for raw data directory, city list file, and output CSV file.
    """
    raw_data_dir = os.path.join("..", "data", "raw")
    os.makedirs(raw_data_dir, exist_ok=True)

    paths = {
        "raw_data_dir": raw_data_dir,
        "city_list": os.path.join(raw_data_dir, "haunted_places_list.csv"),
        "sun_data_file": os.path.join(raw_data_dir, "sunrise_sunset_data.csv"),
    }
    return paths


# Main Function
def main():
    """Main function to execute the script with predefined paths."""
    paths = define_paths()

    # Load city list
    cities_df = pd.read_csv(paths["city_list"])
    cities = cities_df["city"].unique()

    # Base URL
    base_url = "https://www.timeanddate.com/sun/usa/"

    # Initialize list for storing results
    data = []

    # Loop through cities and scrape data
    for city in cities:
        url = f"{base_url}{city}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract sunrise and sunset times
            try:
                sunrise = soup.find("td", class_="c sep-l").text.strip()
                sunset = soup.find("td", class_="c").find_next_sibling("td").text.strip()
                print(f"Scraped {city.capitalize()}: Sunrise {sunrise}, Sunset {sunset}")
                data.append([city.replace("-", " ").title(), sunrise, sunset])
            except AttributeError:
                print(f"Could not extract data for {city}")

        else:
            print(f"Failed to retrieve {city}, Status Code: {response.status_code}")

    # Convert to DataFrame
    sun_data_df = pd.DataFrame(data, columns=["City", "Sunrise", "Sunset"])

    # Save to CSV
    sun_data_df.to_csv(paths["sun_data_file"], index=False)
    print(f"Sunrise and sunset data saved at: {paths['sun_data_file']}")
    # Save a copy of TSV
    sun_data_df.to_csv(paths["sun_data_file"].replace(".csv", ".tsv"), sep="\t", index=False)
    print(f"Sunrise and sunset data saved at: {paths['sun_data_file'].replace('.csv', '.tsv')}")



# Execute Main Function
if __name__ == "__main__":
    main()
