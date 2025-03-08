import os
import json
import pandas as pd

# Step 1: Define relative paths
data_dir = os.path.join('..', 'data', 'raw')  # Save to "raw" inside "data"

# Ensure the directory exists
os.makedirs(data_dir, exist_ok=True)

# Define file paths
input_file = os.path.join(data_dir, 'Violent Crime & Property Crime Statewide Totals.json')  # JSON input file
output_csv_file = os.path.join(data_dir, 'Violent_Crime_Property_Crime.csv')  # CSV output file
output_tsv_file = os.path.join(data_dir, 'Violent_Crime_Property_Crime.tsv')  # TSV output file

# Step 2: Load the JSON file
with open(input_file, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Step 3: Extract relevant data
data_records = json_data.get("data", [])

# Define the required columns
required_columns = [
    "JURISDICTION", "YEAR",
    "OVERALL CRIME RATE PER 100,000 PEOPLE", "OVERALL PERCENT CHANGE PER 100,000 PEOPLE",
    "VIOLENT CRIME RATE PER 100,000 PEOPLE", "VIOLENT CRIME RATE PERCENT CHANGE PER 100,000 PEOPLE",
    "PROPERTY CRIME RATE PER 100,000 PEOPLE", "PROPERTY CRIME RATE PERCENT CHANGE PER 100,000 PEOPLE",
    "MURDER PER 100,000 PEOPLE", "RAPE PER 100,000 PEOPLE", "ROBBERY PER 100,000 PEOPLE", "AGG. ASSAULT PER 100,000 PEOPLE",
    "B & E PER 100,000 PEOPLE", "LARCENY THEFT PER 100,000 PEOPLE", "M/V THEFT PER 100,000 PEOPLE",
    "MURDER  RATE PERCENT CHANGE PER 100,000 PEOPLE", "RAPE RATE PERCENT CHANGE PER 100,000 PEOPLE",
    "ROBBERY RATE PERCENT CHANGE PER 100,000 PEOPLE", "AGG. ASSAULT  RATE PERCENT CHANGE PER 100,000 PEOPLE",
    "B & E RATE PERCENT CHANGE PER 100,000 PEOPLE", "LARCENY THEFT  RATE PERCENT CHANGE PER 100,000 PEOPLE",
    "M/V THEFT  RATE PERCENT CHANGE PER 100,000 PEOPLE"
]

# Extract column names from metadata and match with required columns
all_columns = [col["name"] for col in json_data["meta"]["view"]["columns"] if "name" in col]
selected_columns = [col for col in required_columns if col in all_columns]

# Step 4: Create a DataFrame with selected columns
df = pd.DataFrame(data_records, columns=all_columns)  # Load all columns first
df = df[selected_columns]  # Select only required columns

# Step 5: Save to CSV and TSV
df.to_csv(output_csv_file, index=False)  # Save as CSV
df.to_csv(output_tsv_file, index=False, sep='\t')  # Save as TSV

print(f"CSV file with selected columns has been saved to {output_csv_file}")
print(f"TSV file with selected columns has been saved to {output_tsv_file}")
