import os
import pandas as pd


# **Step 1: Define Paths**
def define_paths():
    """
    Defines the relative paths for input and output files.

    Returns:
        dict: A dictionary containing paths for the data directory, CSV file, and TSV file.
    """
    data_dir = os.path.join('..', 'data', 'raw')  # Directory for raw data
    os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists

    paths = {
        "data_dir": data_dir,
        "csv_file": os.path.join(data_dir, 'apportionment.csv'),
        "tsv_file": os.path.join(data_dir, 'apportionment.tsv')
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
        print(f" Error: File not found at {os.path.abspath(file_path)}")
        return False
    return True


# Step 3: Load the CSV File
def load_csv(file_path):
    """
    Loads a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The full path of the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    return pd.read_csv(file_path)


# Step 4: Clean and Process Data
def process_data(df):
    """
    Filters the DataFrame to include only states, converts column names to lowercase, and renames 'name' to 'city'.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    df = df[df['Geography Type'] == 'State']  # Filter only states
    df.columns = df.columns.str.lower()  # Convert column names to lowercase
    df = df.rename(columns={'name': 'city'})  # Rename 'name' column to 'city'
    return df


# **Step 5: Save Processed Data to TSV**
def save_to_tsv(df, output_path):
    """
    Saves the processed DataFrame as a TSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_path (str): The path where the TSV file should be saved.
    """
    df.to_csv(output_path, sep='\t', index=False)
    print(f" File successfully converted to TSV: {os.path.abspath(output_path)}")


# Main Function
def main():
    """Main function to handle the entire data processing workflow."""
    paths = define_paths()

    if not check_file_existence(paths["csv_file"]):
        return

    df = load_csv(paths["csv_file"])
    df = process_data(df)
    save_to_tsv(df, paths["tsv_file"])


# Execute Main Function
if __name__ == "__main__":
    main()
