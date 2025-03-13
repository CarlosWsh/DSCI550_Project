import os
import pandas as pd


def crime_merge(hp_file, ncvs_personal_file, output_file):
    """
    Merges the HP analysis dataset with the crime dataset.

    :param hp_file: Path to the HP analysis file.
    :param ncvs_personal_file: Path to the crime dataset file.
    :param output_file: Path where the merged dataset will be saved.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Check if files exist
    if not os.path.exists(ncvs_personal_file):
        print(f"Error: Missing file {ncvs_personal_file}")
        return
    elif not os.path.exists(hp_file):
        print(f"Error: Missing file {hp_file}")
        return

    # Load TSV files
    ncvs_personal_df = pd.read_csv(ncvs_personal_file, sep="\t")
    hp_df = pd.read_csv(hp_file, sep="\t")

    # Standardize column names (lowercase and strip spaces)
    ncvs_personal_df.columns = ncvs_personal_df.columns.str.strip().str.lower()
    hp_df.columns = hp_df.columns.str.strip().str.lower()

    # Ensure 'year' and 'quarter' exist in both datasets
    common_columns = ["year", "quarter"]
    if not all(col in hp_df.columns for col in common_columns):
        print(f"Error: Columns '{common_columns}' not found in hp_analysis_v2.tsv.")
        return
    elif not all(col in ncvs_personal_df.columns for col in common_columns):
        print(f"Error: Columns '{common_columns}' not found in ncvs_personal_engineered.tsv.")
        return

    # Convert 'year' and 'quarter' to integer if needed (to avoid mismatches)
    for col in common_columns:
        hp_df[col] = pd.to_numeric(hp_df[col], errors="coerce")
        ncvs_personal_df[col] = pd.to_numeric(ncvs_personal_df[col], errors="coerce")

    # Merge datasets using LEFT JOIN to keep all HP Analysis v2 records
    merged_df = pd.merge(hp_df, ncvs_personal_df, on=common_columns, how="left")

    # Save to new TSV file
    merged_df.to_csv(output_file, sep="\t", index=False)
    print(f"Merged TSV file saved at: {os.path.abspath(output_file)}")


# Define file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
RAW_DIR = os.path.join(BASE_DIR, "data", "processed")  # Should this be 'raw'?

ncvs_personal_file = os.path.join(RAW_DIR, "ncvs_personal_engineered.tsv")
hp_file = os.path.join(PROCESSED_DIR, "hp_analysis_v2.tsv")
output_file = os.path.join(PROCESSED_DIR, "hp_analysis_crime.tsv")

# Run the function
crime_merge(hp_file, ncvs_personal_file, output_file)