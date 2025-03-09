import os
import pandas as pd


# **Step 1: Define Paths**
def define_paths():
    """
    Defines the relative paths for input and output files.

    Returns:
        dict: A dictionary containing paths for data directory, input CSV file, TSV file, and the filtered list CSV file.
    """
    data_dir = os.path.join('..', 'data', 'raw')  # Directory for raw data
    os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists

    paths = {
        "data_dir": data_dir,
        "csv_file": os.path.join(data_dir, 'haunted_places.csv'),
        "tsv_file": os.path.join(data_dir, 'haunted_places.tsv'),
        "filtered_list": os.path.join(data_dir, 'haunted_places_list.csv')
    }
    return paths


# **Step 2: Check File Existence**
def check_file_existence(file_path):
    """
    Checks whether a file exists.

    Args:
        file_path (str): The full path of the file.

    Returns:
        bool: True if the file exists, otherwise False.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {os.path.abspath(file_path)}")
        return False
    return True


# **Step 3: Load the CSV File with Explicit Data Types**
def load_csv(file_path):
    """
    Loads a CSV file into a Pandas DataFrame with predefined data types.

    Args:
        file_path (str): The full path of the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    dtype_mapping = {
        "city": "string",
        "country": "string",
        "description": "string",
        "location": "string",
        "state": "string",
        "state_abbrev": "string",
        "longitude": "float64",
        "latitude": "float64",
        "city_longitude": "float64",
        "city_latitude": "float64",
    }

    try:
        df = pd.read_csv(file_path, dtype=dtype_mapping, low_memory=False)
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None

    return df


# **Step 4: Convert CSV to TSV**
def convert_csv_to_tsv(df, output_path):
    """
    Converts a DataFrame to a TSV (Tab-Separated Values) file.

    Args:
        df (pd.DataFrame): The DataFrame to convert.
        output_path (str): The path where the TSV file should be saved.
    """
    df.to_csv(output_path, sep='\t', index=False)
    print(f"✅ File successfully converted to TSV: {os.path.abspath(output_path)}")


# **Step 5: Generate a Filtered List (City, Country, State, State Abbreviation)**
def extract_location_columns(df, output_path):
    """
    Extracts and saves a list of city, country, state, and state abbreviation.

    Args:
        df (pd.DataFrame): The DataFrame containing the original data.
        output_path (str): The path where the filtered list should be saved.
    """
    location_columns = ['city', 'country', 'state', 'state_abbrev']

    # Ensure the required columns exist before selecting them
    available_columns = [col for col in location_columns if col in df.columns]

    if not available_columns:
        print("❌ Error: None of the expected location columns found in the dataset.")
        return

    df_filtered = df[available_columns].fillna("Unknown")
    df_filtered.to_csv(output_path, index=False)
    print(f"✅ Filtered location data saved: {os.path.abspath(output_path)}")


# **Main Function**
def main():
    """Main function to handle the entire data processing workflow."""
    paths = define_paths()

    if not check_file_existence(paths["csv_file"]):
        return

    df = load_csv(paths["csv_file"])
    if df is None:
        return  # Exit if CSV loading fails

    convert_csv_to_tsv(df, paths["tsv_file"])
    extract_location_columns(df, paths["filtered_list"])

    # print data types
    print(df.dtypes)

# **Execute Main Function**
if __name__ == "__main__":
    main()
