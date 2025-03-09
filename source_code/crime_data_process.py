import os
import json
import pandas as pd


# Step 1: Define Paths
def define_paths():
    """
    Defines the relative paths for input and output files.

    Returns:
        dict: A dictionary containing paths for the data directory, JSON input file, CSV output file, and TSV output file.
    """
    data_dir = os.path.join('..', 'data', 'raw')  # Directory for raw data
    os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists

    paths = {
        "data_dir": data_dir,
        "json_file": os.path.join(data_dir, 'Violent Crime & Property Crime Statewide Totals.json'),
        "csv_file": os.path.join(data_dir, 'Violent_Crime_Property_Crime.csv'),
        "tsv_file": os.path.join(data_dir, 'Violent_Crime_Property_Crime.tsv')
    }
    return paths


# Step 2: Check File Existence
def check_file_existence(file_path):
    """
    Checks whether a file exists.

    Args:
        file_path (str): The full path of the file.

    Returns:
        bool: True if the file exists, otherwise False.
    """
    if not os.path.exists(file_path):
        print(f" Error: File not found at {os.path.abspath(file_path)}")
        return False
    return True


# Step 3: Load JSON File
def load_json(file_path):
    """
    Loads a JSON file.

    Args:
        file_path (str): The full path of the JSON file.

    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Step 4: Extract Data
def extract_data(json_data):
    """
    Extracts relevant data from the JSON file.

    Args:
        json_data (dict): The JSON data loaded from the file.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted data.
    """
    data_records = json_data.get("data", [])

    required_columns = [
        "JURISDICTION", "YEAR",
        "OVERALL CRIME RATE PER 100,000 PEOPLE", "OVERALL PERCENT CHANGE PER 100,000 PEOPLE",
        "VIOLENT CRIME RATE PER 100,000 PEOPLE", "VIOLENT CRIME RATE PERCENT CHANGE PER 100,000 PEOPLE",
        "PROPERTY CRIME RATE PER 100,000 PEOPLE", "PROPERTY CRIME RATE PERCENT CHANGE PER 100,000 PEOPLE",
        "MURDER PER 100,000 PEOPLE", "RAPE PER 100,000 PEOPLE", "ROBBERY PER 100,000 PEOPLE", "AGG. ASSAULT PER 100,000 PEOPLE",
        "B & E PER 100,000 PEOPLE", "LARCENY THEFT PER 100,000 PEOPLE", "M/V THEFT PER 100,000 PEOPLE",
        "MURDER  RATE PERCENT CHANGE PER 100,000 PEOPLE", "RAPE RATE PERCENT CHANGE PER 100,000 PEOPLE",
        "ROBBERY RATE PERCENT CHANGE PER 100,000 PEOPLE", "AGG. ASSAULT  RATE PERCENT CHANGE PER 100,000 PEOPLE",
        "B & E RATE PERCENT CHANGE PER 100,000 PEOPLE", "LARCENY THEFT  RATE PERCENT CHANGE PER 100,000 PEOPLE",
        "M/V THEFT  RATE PERCENT CHANGE PER 100,000 PEOPLE"
    ]

    # Extract column names from metadata
    all_columns = [col["name"] for col in json_data["meta"]["view"]["columns"] if "name" in col]

    # Select only the required columns that exist in the dataset
    selected_columns = [col for col in required_columns if col in all_columns]

    # Create DataFrame and select required columns
    df = pd.DataFrame(data_records, columns=all_columns)
    return df[selected_columns] if selected_columns else pd.DataFrame()


# Step 5: Save Processed Data to CSV and TSV
def save_data(df, csv_path, tsv_path):
    """
    Saves the extracted DataFrame to CSV and TSV files.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        csv_path (str): The path where the CSV file should be saved.
        tsv_path (str): The path where the TSV file should be saved.
    """
    df.to_csv(csv_path, index=False)
    df.to_csv(tsv_path, index=False, sep='\t')
    print(f" CSV file saved: {os.path.abspath(csv_path)}")
    print(f" TSV file saved: {os.path.abspath(tsv_path)}")


# Main Function
def main():
    """Main function to process the violent crime and property crime dataset."""
    paths = define_paths()

    if not check_file_existence(paths["json_file"]):
        return

    json_data = load_json(paths["json_file"])
    df = extract_data(json_data)

    if df.empty:
        print("⚠ No valid data extracted. Please check the dataset format.")
        return

    save_data(df, paths["csv_file"], paths["tsv_file"])


# Execute Main Function
if __name__ == "__main__":
    main()
