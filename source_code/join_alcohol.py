import os
import pandas as pd

# Define file paths
processed_dir = os.path.join("..", "data", "processed")  # Directory for HP analysis data
raw_dir = os.path.join("..", "data", "raw")  # Directory for alcohol data

hp_file = os.path.join(processed_dir, "hp_analysis_v2.tsv")  # HP analysis file
alcohol_file = os.path.join(raw_dir, "state_alcohol_abuse.tsv")  # Alcohol data file
output_file = os.path.join(processed_dir, "hp_analysis_alcohol.tsv")  # Merged output

# Check if files exist
if not os.path.exists(hp_file) or not os.path.exists(alcohol_file):
    print("❌ Error: One or both input files are missing.")
else:
    # Load TSV files
    hp_df = pd.read_csv(hp_file, sep="\t")
    alcohol_df = pd.read_csv(alcohol_file, sep="\t")

    # Print column names for debugging
    print("📌 Columns in hp_analysis_v2.tsv:", hp_df.columns.tolist())
    print("📌 Columns in state_alcohol_abuse.tsv:", alcohol_df.columns.tolist())

    # Trim spaces and standardize column names to lowercase
    hp_df.columns = hp_df.columns.str.strip().str.lower()
    alcohol_df.columns = alcohol_df.columns.str.strip().str.lower()

    # Determine the common column (now using lowercase 'state')
    common_column = "state"
    if common_column not in hp_df.columns or common_column not in alcohol_df.columns:
        print(f"❌ Error: Column '{common_column}' not found in one of the files.")
    else:
        # Merge the datasets on the common column
        merged_df = pd.merge(hp_df, alcohol_df, on=common_column, how="left")

        # Save to new TSV file
        merged_df.to_csv(output_file, sep="\t", index=False)
        print(f"✅ Merged TSV file saved at: {os.path.abspath(output_file)}")
