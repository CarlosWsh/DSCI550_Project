import pandas as pd
import os

# Step 1: Define relative paths
data_dir = os.path.join('..', 'data', 'raw')  # Save to "raw" inside "data"

# Ensure the directory exists
os.makedirs(data_dir, exist_ok=True)

# Define file paths
input_file = os.path.join('..', 'data', 'raw', 'apportionment.csv')  # Assuming CSV is also in "raw"
output_file = os.path.join(data_dir, 'apportionment.tsv')

# Step 2: Check if the file exists before attempting to read
if not os.path.exists(input_file):
    print(f"Error: File not found at {os.path.abspath(input_file)}")
    exit(1)

# Step 3: Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)
print(f"File loaded successfully from: {os.path.abspath(input_file)}")

# filter geography type to only include states
df = df[df['Geography Type'] == 'State']

# column name to lowercase
df.columns = df.columns.str.lower()

# rename name to city
df = df.rename(columns={'name': 'city'})

# Step 4: Save the DataFrame as a TSV file inside "raw"
df.to_csv(output_file, sep='\t', index=False)
print(f"File converted successfully: {os.path.abspath(output_file)}")

