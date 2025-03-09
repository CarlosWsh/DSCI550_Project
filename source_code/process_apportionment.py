import os
import pandas as pd

# Step 1: Define Paths
def define_paths():
    """
    Defines the relative paths for input and output files.

    Returns:
        dict: A dictionary containing paths for the data directory, CSV file, and TSV file.
    """
    data_dir = os.path.join("..", "data", "raw")  # Directory for raw data
    os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists

    paths = {
        "data_dir": data_dir,
        "csv_file": os.path.join(data_dir, "apportionment.csv"),
        "tsv_file": os.path.join(data_dir, "apportionment.tsv"),
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
        print(f"❌ Error: File not found at {os.path.abspath(file_path)}")
        return False
    return True

# Step 3: Load the CSV File with Explicit Data Types
def load_csv(file_path):
    """
    Loads a CSV file into a Pandas DataFrame with predefined data types.

    Args:
        file_path (str): The full path of the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    try:
        df = pd.read_csv(file_path, low_memory=False)

        # Standardize column names: lowercase and replace spaces with underscores
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        # Convert columns with comma-separated numbers to integers
        numeric_columns = [
            "resident_population",
            "average_apportionment_population_per_representative",
        ]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")

        # Convert float-based columns
        float_columns = [
            "percent_change_in_resident_population",
            "resident_population_density_rank",
            "resident_population_density",
            "change_in_number_of_representatives",
        ]
        for col in float_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None

# Step 4: Clean and Process Data
def process_data(df):
    """
    Filters the DataFrame to include only states, renames columns, and handles missing values.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    if "geography_type" in df.columns:
        df = df[df["geography_type"] == "State"]  # Filter only states

    # Rename 'name' to 'city' if present
    if "name" in df.columns:
        df.rename(columns={"name": "city"}, inplace=True)

    # Fill missing values
    for col in df.select_dtypes(include=["string"]).columns:
        df[col] = df[col].fillna("Unknown").str.strip()

    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        df[col] = df[col].fillna(0)

    return df

# Step 5: Save Processed Data to TSV
def save_to_tsv(df, output_path):
    """
    Saves the processed DataFrame as a TSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_path (str): The path where the TSV file should be saved.
    """
    df.to_csv(output_path, sep="\t", index=False)
    print(f"✅ File successfully converted to TSV: {os.path.abspath(output_path)}")

# Main Function
def main():
    """Main function to handle the entire data processing workflow."""
    paths = define_paths()

    if not check_file_existence(paths["csv_file"]):
        return

    df = load_csv(paths["csv_file"])
    if df is None:
        return  # Exit if CSV loading fails

    df = process_data(df)
    save_to_tsv(df, paths["tsv_file"])

    # Print DataFrame dtypes for debugging
    print(df.dtypes)

# Execute Main Function
if __name__ == "__main__":
    main()
