import os
import pandas as pd

# Step 1: Define Paths
def define_paths():
    """
    Defines the relative paths for input TSV files and output merged TSV file.

    Returns:
        dict: A dictionary containing paths for both input files and the output file.
    """
    data_dir = os.path.join("..", "data", "processed")  # Ensure processed data directory
    os.makedirs(data_dir, exist_ok=True)  # Ensure directory exists

    paths = {
        "file1": os.path.join(data_dir, "hp_with_date_and_witness_count.tsv"),
        "file2": os.path.join(data_dir, "hp_analysis_v1.tsv"),
        "output_file": os.path.join(data_dir, "hp_analysis_v2.tsv"),
    }
    return paths


# Step 2: Merge, Format, and Clean Data
def merge_and_clean_data(file1_path, file2_path, output_path):
    """
    Merges only the 'HP_date' and 'Witness_count' columns from hp_with_date_and_witness_count.tsv
    into hp_analysis_v1.tsv, removes 'Haunted_Place_Date' & 'Witness_Count', and formats 'HP_date'.

    Args:
        file1_path (str): Path to the first TSV file.
        file2_path (str): Path to the second TSV file.
        output_path (str): Path to save the merged and cleaned TSV file.
    """
    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        print("Error: One or both input files are missing.")
        return

    df1 = pd.read_csv(file1_path, sep="\t")
    df2 = pd.read_csv(file2_path, sep="\t")

    # Print column names for debugging
    print("Columns in hp_with_date_and_witness_count.tsv:", df1.columns.tolist())
    print("Columns in hp_analysis_v1.tsv:", df2.columns.tolist())

    # Trim spaces and standardize column names
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Ensure the required columns exist
    required_columns = ["description", "HP_date", "Witness_count"]
    missing_columns = [col for col in required_columns if col not in df1.columns]

    if missing_columns:
        print(f"Error: Missing columns in hp_with_date_and_witness_count.tsv -> {missing_columns}")
        return

    # Keep only 'description', 'HP_date', and 'Witness_count'
    df1_selected = df1[["description", "HP_date", "Witness_count"]]

    # Merge only these columns into df2
    merged_df = pd.merge(df2, df1_selected, on="description", how="left")

    # **Step 3: Remove Unwanted Columns**
    columns_to_remove = ["Haunted_Place_Date", "Witness_Count"]
    merged_df = merged_df.drop(columns=[col for col in columns_to_remove if col in merged_df.columns], errors='ignore')

    # **Step 4: Format 'HP_date' and Set Nulls to '2025/01/01'**
    merged_df["HP_date"] = pd.to_datetime(merged_df["HP_date"], errors="coerce").dt.strftime("%Y/%m/%d")
    merged_df["HP_date"] = merged_df["HP_date"].fillna("2025/01/01")  # Replace NaN values

    # **Save to new TSV file**
    merged_df.to_csv(output_path, sep="\t", index=False)
    print(f"Merged and cleaned TSV file saved at: {os.path.abspath(output_path)}")


# **Main Function**
def main():
    """Main function to execute the merging process."""
    paths = define_paths()
    merge_and_clean_data(paths["file1"], paths["file2"], paths["output_file"])


# **Execute Main Function**
if __name__ == "__main__":
    main()
