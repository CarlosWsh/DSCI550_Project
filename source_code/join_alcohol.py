import os
import pandas as pd


def alcohol_merge(hp_file, alcohol_file, output_file, common_column="state"):
    """
    Merges the HP analysis dataset with the alcohol abuse dataset.

    :param hp_file: Path to the HP analysis file.
    :param alcohol_file: Path to the alcohol abuse dataset file.
    :param output_file: Path where the merged dataset will be saved.
    :param common_column: Column name on which to merge the datasets (default: "state").
    """
    # Check if files exist
    if not os.path.exists(hp_file) or not os.path.exists(alcohol_file):
        print(f"Error: One or both input files are missing: {hp_file}, {alcohol_file}")
        return

    # Load TSV files
    hp_df = pd.read_csv(hp_file, sep="\t")
    alcohol_df = pd.read_csv(alcohol_file, sep="\t")

    # Standardize column names (trim spaces, lowercase)
    hp_df.columns = hp_df.columns.str.strip().str.lower()
    alcohol_df.columns = alcohol_df.columns.str.strip().str.lower()

    # Verify that the common column exists
    if common_column not in hp_df.columns or common_column not in alcohol_df.columns:
        print(f"Error: Column '{common_column}' not found in one of the files.")
        return

    # Merge datasets
    merged_df = pd.merge(hp_df, alcohol_df, on=common_column, how="left")

    # Save to new TSV file
    merged_df.to_csv(output_file, sep="\t", index=False)
    print(f"Merged TSV file saved at: {os.path.abspath(output_file)}")


# Define file paths
processed_dir = os.path.join("..", "data", "processed")
raw_dir = os.path.join("..", "data", "raw")

hp_file = os.path.join(processed_dir, "hp_analysis_v2.tsv")
alcohol_file = os.path.join(raw_dir, "state_alcohol_abuse.tsv")
output_file = os.path.join(processed_dir, "hp_analysis_alcohol.tsv")

# Run the function
alcohol_merge(hp_file, alcohol_file, output_file)
