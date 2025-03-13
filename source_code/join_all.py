import os
import pandas as pd
from join_alcohol import alcohol_merge
from join_apportionment import apportionment_merge
from join_crime import crime_merge
from join_daytime import daytime_merge
from join_tribes import tribes_merge

def merge_all():
    """
    Runs all merge functions and combines the datasets into a final merged file.
    """
    # Define directories
    processed_dir = os.path.join("..", "data", "processed")
    raw_dir = os.path.join("..", "data", "raw")

    # Define file paths
    hp_file = os.path.join(processed_dir, "hp_analysis_v2.tsv")
    final_output_file = os.path.join(processed_dir, "hp_analysis_final.tsv")

    # Merge each dataset separately
    alcohol_output = os.path.join(processed_dir, "hp_analysis_alcohol.tsv")
    apportionment_output = os.path.join(processed_dir, "hp_analysis_apportionment.tsv")
    crime_output = os.path.join(processed_dir, "hp_analysis_crime.tsv")
    daytime_output = os.path.join(processed_dir, "hp_analysis_daytime.tsv")
    tribes_output = os.path.join(processed_dir, "hp_analysis_tribes.tsv")

    # Run individual merges
    alcohol_merge(hp_file, os.path.join(raw_dir, "state_alcohol_abuse.tsv"), alcohol_output)
    apportionment_merge(hp_file, os.path.join(raw_dir, "apportionment.tsv"), apportionment_output)
    crime_merge(hp_file, os.path.join(processed_dir, "ncvs_personal_engineered.tsv"), crime_output)
    daytime_merge(hp_file, os.path.join(raw_dir, "sunrise_sunset_data.tsv"), os.path.join(raw_dir, "sun_moon_data_combined.tsv"), daytime_output)
    tribes_merge(hp_file, os.path.join(processed_dir, "tribes_per_state.tsv"), tribes_output)

    # Load all merged datasets
    merged_files = [alcohol_output, apportionment_output, crime_output, daytime_output, tribes_output]
    final_df = None

    for file in merged_files:
        if os.path.exists(file):
            df = pd.read_csv(file, sep="\t")
            if final_df is None:
                final_df = df
            else:
                common_columns = list(set(final_df.columns) & set(df.columns))
                final_df = pd.merge(final_df, df, on=common_columns, how="outer")
        else:
            print(f"Warning: {file} not found, skipping merge.")

    #rename column haunted_place_date to hp_date
    final_df.rename(columns = {'haunted_place_date':'hp_date'}, inplace = True)
    # Save the final merged dataset
    if final_df is not None:
        final_df.to_csv(final_output_file, sep="\t", index=False)
        print(f"Final merged dataset saved at: {os.path.abspath(final_output_file)}")
    else:
        print("Error: No datasets were successfully merged.")

# Run the function
if __name__ == "__main__":
    merge_all()