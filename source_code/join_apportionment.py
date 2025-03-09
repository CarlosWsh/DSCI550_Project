import os
import pandas as pd

# Define file paths
processed_dir = os.path.join("..", "data", "processed")  # Directory for processed data
raw_dir = os.path.join("..", "data", "raw")  # Directory for raw data

hp_analysis_file = os.path.join(processed_dir, "hp_analysis_v2.tsv")  # HP analysis file
apportionment_file = os.path.join(raw_dir, "apportionment.tsv")  # Apportionment data file
output_file_final = os.path.join(processed_dir, "hp_analysis_apportionment.tsv")  # Final merged output

# Check if files exist
if not os.path.exists(hp_analysis_file) or not os.path.exists(apportionment_file):
    print("❌ Error: One or both input files are missing.")
else:
    # Load TSV files
    hp_df = pd.read_csv(hp_analysis_file, sep="\t")
    apportionment_df = pd.read_csv(apportionment_file, sep="\t")

    # Print column names for debugging
    print("📌 Columns in hp_analysis_v2.tsv:", hp_df.columns.tolist())
    print("📌 Columns in apportionment.tsv:", apportionment_df.columns.tolist())

    # Standardize column names to lowercase and remove spaces
    hp_df.columns = hp_df.columns.str.strip().str.lower()
    apportionment_df.columns = apportionment_df.columns.str.strip().str.lower()

    # Define the common column for merging
    hp_common_column = "state"  # HP dataset uses state
    apportionment_common_column = "city"  # Apportionment dataset uses city
    year_column = "year"  # Ensure year column exists in both

    # Convert year to integer format
    if year_column in hp_df.columns:
        hp_df[year_column] = pd.to_numeric(hp_df[year_column], errors="coerce").astype("Int64")

    if year_column in apportionment_df.columns:
        apportionment_df[year_column] = pd.to_numeric(apportionment_df[year_column], errors="coerce").astype("Int64")

    # Forward-fill missing data for years not explicitly listed
    apportionment_df = apportionment_df.sort_values(by=[apportionment_common_column, year_column])
    apportionment_df = apportionment_df.set_index(year_column).groupby(apportionment_common_column).apply(
        lambda group: group.reindex(range(group.index.min(), group.index.max() + 1)).ffill()
    ).reset_index(level=0, drop=True).reset_index()

    # Verify that the common columns exist
    if hp_common_column not in hp_df.columns or apportionment_common_column not in apportionment_df.columns or year_column not in hp_df.columns or year_column not in apportionment_df.columns:
        print(f"❌ Error: One of the required columns ('{hp_common_column}', '{apportionment_common_column}', '{year_column}') is missing in one of the files.")
    else:
        # Merge the datasets on state abbreviation and year
        final_merged_df = pd.merge(hp_df, apportionment_df, left_on=[hp_common_column, year_column], right_on=[apportionment_common_column, year_column], how="left")

        # Drop the redundant 'city' column (renamed as 'city_y' by Pandas)
        if "city_y" in final_merged_df.columns:
            final_merged_df = final_merged_df.drop(columns=["city_y"])

        # Save the final merged dataset to TSV
        final_merged_df.to_csv(output_file_final, sep="\t", index=False)
        print(f"✅ Final merged TSV file saved at: {os.path.abspath(output_file_final)}")
