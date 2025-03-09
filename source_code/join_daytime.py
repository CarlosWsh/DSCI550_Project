import os
import pandas as pd


def daytime_merge(hp_file, sunrise_sunset_file, sun_moon_file, output_file):
    """
    Merges the HP analysis dataset with sunrise/sunset and sun/moon datasets.

    :param hp_file: Path to the HP analysis file.
    :param sunrise_sunset_file: Path to the sunrise/sunset dataset file.
    :param sun_moon_file: Path to the sun/moon dataset file.
    :param output_file: Path where the merged dataset will be saved.
    """
    # Check if files exist
    if not os.path.exists(hp_file) or not os.path.exists(sunrise_sunset_file) or not os.path.exists(sun_moon_file):
        print("Error: One or more input files are missing.")
        return

    # Load TSV files
    hp_df = pd.read_csv(hp_file, sep="\t")
    sunrise_sunset_df = pd.read_csv(sunrise_sunset_file, sep="\t")
    sun_moon_df = pd.read_csv(sun_moon_file, sep="\t")

    # Standardize column names (lowercase, strip spaces)
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
    print(f"Merged TSV file saved at: {os.path.abspath(output_file)}")


# Define file paths
processed_dir = os.path.join("..", "data", "processed")
raw_dir = os.path.join("..", "data", "raw")

hp_file = os.path.join(processed_dir, "hp_analysis_v2.tsv")
sunrise_sunset_file = os.path.join(raw_dir, "sunrise_sunset_data.tsv")
sun_moon_file = os.path.join(raw_dir, "sun_moon_data_combined.tsv")
output_file = os.path.join(processed_dir, "hp_analysis_daytime.tsv")

# Run the function
daytime_merge(hp_file, sunrise_sunset_file, sun_moon_file, output_file)
