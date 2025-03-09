import os
import pandas as pd

# Define file paths
processed_dir = os.path.join("..", "data", "processed")  # Processed data directory
raw_dir = os.path.join("..", "data", "raw")  # Raw data directory

hp_file = os.path.join(processed_dir, "hp_analysis_v2.tsv")  # HP analysis file
sunrise_sunset_file = os.path.join(raw_dir, "sunrise_sunset_data.tsv")  # Sunrise/Sunset data
sun_moon_file = os.path.join(raw_dir, "sun_moon_data_combined.tsv")  # Sun/Moon data
output_file = os.path.join(processed_dir, "hp_analysis_daytime.tsv")  # Final merged output

# Check if files exist
if not all(os.path.exists(f) for f in [hp_file, sunrise_sunset_file, sun_moon_file]):
    print("❌ Error: One or more input files are missing.")
else:
    # Load TSV files
    hp_df = pd.read_csv(hp_file, sep="\t")
    sunrise_sunset_df = pd.read_csv(sunrise_sunset_file, sep="\t")
    sun_moon_df = pd.read_csv(sun_moon_file, sep="\t")

    # Print column names for debugging
    print("📌 Columns in hp_analysis_v2.tsv:", hp_df.columns.tolist())
    print("📌 Columns in sunrise_sunset_data.tsv:", sunrise_sunset_df.columns.tolist())
    print("📌 Columns in sun_moon_data_combined.tsv:", sun_moon_df.columns.tolist())

    # Trim spaces and standardize column names to lowercase
    hp_df.columns = hp_df.columns.str.strip().str.lower()
    sunrise_sunset_df.columns = sunrise_sunset_df.columns.str.strip().str.lower()
    sun_moon_df.columns = sun_moon_df.columns.str.strip().str.lower()

    # Rename columns in sunrise_sunset_df to avoid conflicts
    sunrise_sunset_df = sunrise_sunset_df.rename(columns={"sunrise": "city_sunrise", "sunset": "city_sunset"})

    # Merge sunrise/sunset data on 'city'
    merged_df = pd.merge(hp_df, sunrise_sunset_df, on="city", how="left")

    # Merge sun/moon data on 'state' and 'year'
    merged_df = pd.merge(merged_df, sun_moon_df, on=["state", "year"], how="left")

    # Save to new TSV file
    merged_df.to_csv(output_file, sep="\t", index=False)
    print(f"✅ Merged TSV file saved at: {os.path.abspath(output_file)}")
