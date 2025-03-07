import os
import pandas as pd

# **Step 1: Define Relative Paths**
data_dir = os.path.join('..', 'data', 'raw')  # Relative path to "data/raw"
os.makedirs(data_dir, exist_ok=True)  # Ensure directory exists

# Define input and output file paths
csv_file_path = os.path.join(data_dir, 'US_Native_American_Indian_Tribes.csv')
tsv_file_path = os.path.join(data_dir, 'US_Native_American_Indian_Tribes.tsv')


# **Step 2: Ensure the CSV file exists**
if not os.path.exists(csv_file_path):
    print(f"❌ Error: File not found at {os.path.abspath(csv_file_path)}")
    exit(1)

# **Step 3: Load the CSV file**
df = pd.read_csv(csv_file_path)

# **Step 4: Standardize Column Names**
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")  # Remove spaces & convert to lowercase
# drop the columns that are not needed
columns_to_drop = ['default_address_1','default_address_2_(in_case_it_has)']
df = df.drop(columns=columns_to_drop)

# **Step 5: Clean the Data**
df = df.drop_duplicates()  # Remove duplicate rows
df = df.dropna(how="all")  # Remove empty rows (if all values in a row are NaN)

# **Step 6: Save as TSV (Tab-Separated Values)**
df.to_csv(tsv_file_path, index=False, sep="\t")

print(f"✅ File successfully cleaned and converted to TSV: {os.path.abspath(tsv_file_path)}")
