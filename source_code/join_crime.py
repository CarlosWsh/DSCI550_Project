import os
import pandas as pd

# Define file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")  # Processed data directory
RAW_DIR = os.path.join(BASE_DIR, "data", "processed")  # Raw data directory (Should it be 'raw'?)

ncvs_personal_file = os.path.join(RAW_DIR, "ncvs_personal_engineered.tsv")  # NCVS personal data file
hp_file = os.path.join(PROCESSED_DIR, "hp_analysis_v2.tsv")  # HP analysis file
output_file = os.path.join(PROCESSED_DIR, "hp_analysis_crime.tsv")  # Merged output

# Ensure output directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Check if files exist
if not os.path.exists(ncvs_personal_file):
    print(f"❌ Error: Missing file {ncvs_personal_file}")
elif not os.path.exists(hp_file):
    print(f"❌ Error: Missing file {hp_file}")
else:
    # Load TSV files
    ncvs_personal_df = pd.read_csv(ncvs_personal_file, sep="\t")
    hp_df = pd.read_csv(hp_file, sep="\t")

    # Print column names for debugging
    print("📌 Columns in ncvs_personal_engineered.tsv:", ncvs_personal_df.columns.tolist())
    print("📌 Columns in hp_analysis_v2.tsv:", hp_df.columns.tolist())

    # Standardize column names (lowercase and strip spaces)
    ncvs_personal_df.columns = ncvs_personal_df.columns.str.strip().str.lower()
    hp_df.columns = hp_df.columns.str.strip().str.lower()

    # Ensure 'year' and 'quarter' exist in both datasets
    common_columns = ["year", "quarter"]
    if not all(col in hp_df.columns for col in common_columns):
        print(f"❌ Error: Columns '{common_columns}' not found in hp_analysis_v2.tsv.")
    elif not all(col in ncvs_personal_df.columns for col in common_columns):
        print(f"❌ Error: Columns '{common_columns}' not found in ncvs_personal_engineered.tsv.")
    else:
        # Convert 'year' and 'quarter' to integer if needed (to avoid mismatches)
        for col in common_columns:
            hp_df[col] = pd.to_numeric(hp_df[col], errors="coerce")
            ncvs_personal_df[col] = pd.to_numeric(ncvs_personal_df[col], errors="coerce")

        # Merge datasets using LEFT JOIN to keep all HP Analysis v2 records
        merged_df = pd.merge(hp_df, ncvs_personal_df, on=common_columns, how="left")

        # Save to new TSV file
        merged_df.to_csv(output_file, sep="\t", index=False)
        print(f"✅ Merged TSV file saved at: {os.path.abspath(output_file)}")
