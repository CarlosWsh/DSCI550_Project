import os
import json
import pandas as pd
import re

# Define the relative directory path
RELATIVE_DIR = os.path.join("..", "data", "raw")


def list_valid_json_files(directory):
    """
    Lists all JSON files in the specified directory that match the expected naming pattern.

    Args:
        directory (str): The directory to scan for JSON files.

    Returns:
        list: A list of valid JSON file names.
    """
    return [
        f for f in os.listdir(directory)
        if f.endswith(".json") and re.match(r"sun_moon_\d{4}\.json", f)  # Matches filenames like 'sun_moon_1700.json'
    ]


def extract_sun_moon_data(file_path):
    """
    Extracts relevant data from a given JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        list: A list of dictionaries containing processed data.
    """
    with open(file_path, "r") as file:
        data = json.load(file)

    extracted_data = []
    for entry in data:
        record = {
            "Year": entry["Year"],
            "State": entry["State"],
            "Latitude": entry["Latitude"],
            "Longitude": entry["Longitude"],
            "curphase": entry["Sun and Moon Data"]["curphase"],
            "fracillum": entry["Sun and Moon Data"]["fracillum"],
            "Moonrise": next(
                (item["time"] for item in entry["Sun and Moon Data"]["moondata"] if item["phen"] == "Rise"), None),
            "Moon_Upper_Transit": next(
                (item["time"] for item in entry["Sun and Moon Data"]["moondata"] if item["phen"] == "Upper Transit"),
                None),
            "Moonset": next((item["time"] for item in entry["Sun and Moon Data"]["moondata"] if item["phen"] == "Set"),
                            None),
            "Sunrise": next((item["time"] for item in entry["Sun and Moon Data"]["sundata"] if item["phen"] == "Rise"),
                            None),
            "Sun_Upper_Transit": next(
                (item["time"] for item in entry["Sun and Moon Data"]["sundata"] if item["phen"] == "Upper Transit"),
                None),
            "Sunset": next((item["time"] for item in entry["Sun and Moon Data"]["sundata"] if item["phen"] == "Set"),
                           None),
            "Begin_Civil_Twilight": next((item["time"] for item in entry["Sun and Moon Data"]["sundata"] if
                                          item["phen"] == "Begin Civil Twilight"), None),
            "End_Civil_Twilight": next((item["time"] for item in entry["Sun and Moon Data"]["sundata"] if
                                        item["phen"] == "End Civil Twilight"), None),
            "Timezone": entry["Sun and Moon Data"]["tz"]
        }
        extracted_data.append(record)

    return extracted_data


def save_data_to_files(data, directory, filename_prefix="sun_moon_data_combined"):
    """
    Saves the extracted data to CSV and TSV files.

    Args:
        data (list): The processed data in list-of-dictionaries format.
        directory (str): The directory to save the files.
        filename_prefix (str): Prefix for the output file names (default: 'sun_moon_data_combined').

    Returns:
        tuple: Paths of the saved CSV and TSV files.
    """
    df = pd.DataFrame(data)

    # Define explicit data types
    dtype_mapping = {
        "Year": "int64",
        "State": "string",
        "Latitude": "float64",
        "Longitude": "float64",
        "curphase": "string",
        "fracillum": "string",
        "Moonrise": "string",
        "Moon_Upper_Transit": "string",
        "Moonset": "string",
        "Sunrise": "string",
        "Sun_Upper_Transit": "string",
        "Sunset": "string",
        "Begin_Civil_Twilight": "string",
        "End_Civil_Twilight": "string",
        "Timezone": "string"  # Explicitly ensure Timezone is treated as a string
    }

    # Apply data types
    for col, dtype in dtype_mapping.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype, errors="ignore")

    csv_path = os.path.join(directory, f"{filename_prefix}.csv")
    tsv_path = os.path.join(directory, f"{filename_prefix}.tsv")

    df.to_csv(csv_path, index=False)
    df.to_csv(tsv_path, sep="\t", index=False)

    print(df.dtypes)  # Debugging: Print column data types

    return csv_path, tsv_path


def main():
    """Main function to process sun and moon JSON files and save combined results."""
    json_files = list_valid_json_files(RELATIVE_DIR)

    all_data = []
    for json_file in json_files:
        file_path = os.path.join(RELATIVE_DIR, json_file)
        all_data.extend(extract_sun_moon_data(file_path))

    csv_path, tsv_path = save_data_to_files(all_data, RELATIVE_DIR)

    print(f"CSV saved to: {csv_path}")
    print(f"TSV saved to: {tsv_path}")


if __name__ == "__main__":
    main()

