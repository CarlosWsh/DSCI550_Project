import os
import pandas as pd


# Step 1: Define Paths
def define_paths():
    """
    Defines the relative paths for input and output files.

    Returns:
        dict: A dictionary containing paths for the data directory, CSV file, and TSV file.
    """
    data_dir = os.path.join('..', 'data', 'raw')  # Relative path to "data/raw"
    os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists

    paths = {
        "data_dir": data_dir,
        "csv_file": os.path.join(data_dir, 'US_Native_American_Indian_Tribes.csv'),
        "tsv_file": os.path.join(data_dir, 'US_Native_American_Indian_Tribes.tsv')
    }
    return paths


# Step 2: Check if the CSV file exists
def check_file_existence(file_path):
    """
    Checks if a file exists at the specified path.

    Args:
        file_path (str): The full path of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {os.path.abspath(file_path)}")
        return False
    return True


# Step 3: Load the CSV file
def load_csv(file_path):
    """
    Loads a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The full path of the CSV file to load.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    return pd.read_csv(file_path)


# Step 4: Standardize Column Names
def standardize_column_names(df):
    """
    Standardizes column names by converting to lowercase and replacing spaces with underscores.

    Args:
        df (pd.DataFrame): The DataFrame to modify.

    Returns:
        pd.DataFrame: The modified DataFrame with standardized column names.
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")  # Remove spaces & convert to lowercase
    return df


# Step 5: Clean the Data
def clean_data(df):
    """
    Cleans the DataFrame by removing duplicates and empty rows, and dropping unnecessary columns.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    columns_to_drop = ['default_address_1', 'default_address_2_(in_case_it_has)']
    df = df.drop(columns=columns_to_drop, errors='ignore')  # Drop specified columns (ignore if not present)
    df = df.drop_duplicates()  # Remove duplicate rows
    df = df.dropna(how="all")  # Remove empty rows (if all values in a row are NaN)
    return df


# Step 6: Save as TSV (Tab-Separated Values)
def save_to_tsv(df, file_path):
    """
    Saves the cleaned DataFrame as a TSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_path (str): The full path where the TSV file should be saved.
    """
    df.to_csv(file_path, index=False, sep="\t")
    print(f" File successfully cleaned and converted to TSV: {os.path.abspath(file_path)}")


# Main Function
def main():
    """Main function to handle the entire CSV-to-TSV conversion process."""
    paths = define_paths()

    if not check_file_existence(paths["csv_file"]):
        return

    df = load_csv(paths["csv_file"])
    df = standardize_column_names(df)
    df = clean_data(df)
    save_to_tsv(df, paths["tsv_file"])


# Execute Main Function
if __name__ == "__main__":
    main()
