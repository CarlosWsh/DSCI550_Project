import pandas as pd
import os

# Define relative file paths
base_path = os.path.join("..","data", "processed")
input_file = os.path.join(base_path, "hp_analysis_hw2.tsv")
output_file = os.path.join(base_path, "hp_analysis_hw2.tsv")
columns_output_file = os.path.join(base_path, "hp_analysis_final_columns.txt")

# Read the TSV file, dropping unnamed index columns if they exist
df = pd.read_csv(input_file, sep='\t')

# Drop any unwanted 'Unnamed' columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Rename column
df.rename(columns={'hp_date': 'hp_day'}, inplace=True)

# Save the updated DataFrame back to TSV format without index
df.to_csv(output_file, sep='\t', index=False)

# Read the saved TSV file again to confirm the column names
df = pd.read_csv(output_file, sep='\t')

# Save column names to a text file
with open(columns_output_file, 'w') as f:
    for col in df.columns:
        f.write(f"{col}\n")

# Print the column names for verification
print(df.columns.to_list())

