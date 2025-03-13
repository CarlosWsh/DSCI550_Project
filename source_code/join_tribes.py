import os
import pandas as pd


def tribes_merge(hp_analysis_file, state_tribes_file, output_file_final):
    """
    Merges the HP analysis dataset with the state tribes dataset.

    :param hp_analysis_file: Path to the HP analysis file.
    :param state_tribes_file: Path to the tribes dataset file.
    :param output_file_final: Path where the merged dataset will be saved.
    """
    # Check if files exist
    if not os.path.exists(hp_analysis_file) or not os.path.exists(state_tribes_file):
        print(f"Error: One or both input files are missing: {hp_analysis_file}, {state_tribes_file}")
        return

    # Load TSV files
    hp_df = pd.read_csv(hp_analysis_file, sep="\t")
    state_tribes_df = pd.read_csv(state_tribes_file, sep="\t")

    # Standardize column names (lowercase, strip spaces)
    hp_df.columns = hp_df.columns.str.strip().str.lower()
    state_tribes_df.columns = state_tribes_df.columns.str.strip().str.lower()

    # Define the common columns for merging
    hp_common_column = "state_abbrev"  # HP dataset uses state abbreviations
    tribes_common_column = "state"  # Tribes dataset uses full state names

    if hp_common_column not in hp_df.columns or tribes_common_column not in state_tribes_df.columns:
        print(f"Error: Columns '{hp_common_column}' or '{tribes_common_column}' not found in one of the files.")
        return

    # Merge the HP analysis dataset with the tribes per state dataset
    final_merged_df = pd.merge(hp_df, state_tribes_df, left_on=hp_common_column, right_on=tribes_common_column,
                               how="left")

    # Save the final merged dataset to TSV
    final_merged_df.to_csv(output_file_final, sep="\t", index=False)
    print(f"Final merged TSV file saved at: {os.path.abspath(output_file_final)}")


# Define file paths
processed_dir = os.path.join("..", "data", "processed")

hp_analysis_file = os.path.join(processed_dir, "hp_analysis_v2.tsv")
state_tribes_file = os.path.join(processed_dir, "tribes_per_state.tsv")
output_file_final = os.path.join(processed_dir, "hp_analysis_tribes.tsv")

# Run the function
tribes_merge(hp_analysis_file, state_tribes_file, output_file_final)
