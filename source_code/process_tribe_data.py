import os
import pandas as pd


# Step 1: Define Paths
def define_paths():
    """
    Defines the paths for input and output files.

    Returns:
        dict: A dictionary containing paths for the data directory, CSV file, and processed TSV file.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Root directory
    raw_dir = os.path.join(base_dir, "data", "raw")  # Raw data directory
    processed_dir = os.path.join(base_dir, "data", "processed")  # Processed data directory

    # Ensure directories exist
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    paths = {
        "csv_file": os.path.join(raw_dir, "US_Native_American_Indian_Tribes.csv"),
        "tsv_file": os.path.join(raw_dir, "US_Native_American_Indian_Tribes.tsv"),
        "state_stats_file": os.path.join(processed_dir, "tribes_per_state.tsv"),  # File for state-level stats
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
        print(f"Error: File not found at {os.path.abspath(file_path)}")
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
    columns_to_drop = ['default_address_1', 'default_address_2_(in_case_it_has)']  # Columns to remove
    df = df.drop(columns=columns_to_drop, errors='ignore')  # Drop columns (ignore if not present)
    df = df.drop_duplicates()  # Remove duplicate rows
    df = df.dropna(how="all")  # Remove empty rows (if all values in a row are NaN)
    return df


# Step 6: Generate Calculated Features
def generate_features(df):
    """
    Generates calculated features, including:
    - Number of tribes per state with USGS region
    - Percentage of total tribes per state
    - Number of tribes per city

    Args:
        df (pd.DataFrame): The cleaned DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing state and city-level statistics.
    """
    # Count number of tribes per state and include USGS region
    state_counts = df.groupby(["default_state_province", "usgs_region"]).size().reset_index(name="number_of_tribes")

    # Convert state and usgs_region to string
    state_counts["state"] = state_counts["default_state_province"].astype("string")
    state_counts["usgs_region"] = state_counts["usgs_region"].astype("string")

    # Calculate the percentage of total tribes per state
    state_counts["percentage_of_total_tribes"] = (state_counts["number_of_tribes"] / state_counts["number_of_tribes"].sum()) * 100

    # Rename columns for clarity
    state_counts.rename(columns={"default_state_province": "state"}, inplace=True)

    return state_counts


# Step 7: Save as TSV (Tab-Separated Values)
def save_to_tsv(df, file_path):
    """
    Saves the DataFrame as a TSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_path (str): The full path where the TSV file should be saved.
    """
    df.to_csv(file_path, index=False, sep="\t")
    print(f"File successfully saved to TSV: {os.path.abspath(file_path)}")


# Main Function
def main():
    """Main function to handle the entire CSV-to-TSV conversion process with feature calculations."""
    paths = define_paths()

    if not check_file_existence(paths["csv_file"]):
        return

    df = load_csv(paths["csv_file"])
    df = standardize_column_names(df)
    df = clean_data(df)

    # Generate calculated features
    state_stats = generate_features(df)

    # Save cleaned dataset
    save_to_tsv(df, paths["tsv_file"])

    # Save calculated statistics
    save_to_tsv(state_stats, paths["state_stats_file"])


# Execute Main Function
if __name__ == "__main__":
    main()
