import os
import json
import pandas as pd

# Define absolute paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "raw")  # Change to "raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure the output directory exists

# Define file mappings for personal and household data
PERSONAL_FILES = [
    f"ncvs_personal_victimization_{year}.json" for year in range(1993, 2024)
] + [
    f"ncvs_personal_population_{year}.json" for year in range(1993, 2024)
]

# Define variable name to descriptive name mapping from the codebook
column_rename_mappings = {
    "idper": "Person ID",
    "yearq": "Year and Quarter",
    "year": "Year",
    "ager": "Age",
    "sex": "Sex",
    "hispanic": "Hispanic Origin",
    "race": "Race",
    "race_ethnicity": "Race/Hispanic Origin",
    "hincome1": "Annual Household Income",
    "hincome2": "Annual Household Income (Imputed)",
    "marital": "Marital Status",
    "popsize": "Population Size",
    "region": "Region",
    "msa": "Household MSA",
    "locality": "Household Locale",
    "educatn1": "Education Level",
    "educatn2": "Education Level (Extended)",
    "veteran": "Veteran Status",
    "citizen": "Citizenship Status",
    "newcrime": "Aggregate Type of Crime",
    "newoff": "Type of Crime",
    "seriousviolent": "Violent Crime Excluding Simple Assault",
    "notify": "Reporting to Police",
    "vicservices": "Victim Services",
    "locationr": "Location of Crime",
    "direl": "Victim-Offender Relationship",
    "weapon": "Presence of Weapon",
    "weapcat": "Weapon Category",
    "injury": "Injury",
    "serious": "Type of Injury",
    "treatment": "Medical Treatment for Injuries",
    "offenderage": "Offender Age",
    "offendersex": "Offender Sex",
    "offtracenew": "Offender Race/Hispanic Origin",
    "wgtviccy": "Victimization Weight",
    "series": "Series Crime Indicator",
    "newwgt": "Series Adjusted Victimization Weight",
    "wgtpercy": "Person Population Weight",
}

# Define value mappings based on the codebook
value_mappings = {
    "Age": {1: "12-17", 2: "18-24", 3: "25-34", 4: "35-49", 5: "50-64", 6: "65 or older"},
    "Sex": {1: "Male", 2: "Female"},
    "Hispanic Origin": {1: "Hispanic", 2: "Non-Hispanic", 98: "Residue"},
    "Race": {1: "White", 2: "Black", 3: "American Indian/Alaska Native", 4: "Asian/Native Hawaiian/Other Pacific Islander", 5: "More than one race"},
    "Race/Hispanic Origin": {
        1: "Non-Hispanic white",
        2: "Non-Hispanic black",
        3: "Non-Hispanic American Indian/Alaska Native",
        4: "Non-Hispanic Asian/Native Hawaiian/Other Pacific Islander",
        5: "Non-Hispanic more than one race",
        6: "Hispanic",
    },
    "Annual Household Income": {
        1: "Less than $7,500",
        2: "$7,500 to $14,999",
        3: "$15,000 to $24,999",
        4: "$25,000 to $34,999",
        5: "$35,000 to $49,999",
        6: "$50,000 to $74,999",
        7: "$75,000 or more",
        98: "Residue",
    },
    "Annual Household Income (Imputed)": {
        -1: "Invalid until 2017 Q1",
        1: "Less than $25,000",
        2: "$25,000 to $49,999",
        3: "$50,000 to $99,999",
        4: "$100,000 to $199,999",
        5: "$200,000 or more",
    },
    "Marital Status": {1: "Never married", 2: "Married", 3: "Widowed", 4: "Divorced", 5: "Separated", 98: "Residue"},
    "Population Size": {-1: "Invalid until 1995 Q3", 0: "Not a place", 1: "Under 100,000", 2: "100,000-249,999", 3: "250,000-499,999", 4: "500,000-999,999", 5: "1 million or more"},
    "Region": {-1: "Invalid until 1995 Q3", 1: "Northeast", 2: "Midwest", 3: "South", 4: "West"},
    "Household MSA": {1: "Principal city within MSA", 2: "Not part of principal city within MSA", 3: "Outside MSA"},
    "Household Locale": {-1: "Invalid until 2020 Q1", 1: "Urban", 2: "Suburban", 3: "Rural"},
    "Education Level": {1: "No schooling", 2: "Grade school", 3: "Middle school", 4: "High school", 5: "College", 98: "Residue"},
    "Education Level (Extended)": {
        -1: "Invalid until 2003 Q1",
        1: "No schooling",
        2: "Grade school",
        3: "Middle school",
        4: "Some High school",
        5: "High school graduate",
        6: "Some college and associate degree",
        7: "Bachelor’s degree",
        8: "Advanced degree",
        98: "Residue"
    },
    "Veteran Status": {-2: "Invalid until 2017 Q1", -1: "Under age 18", 0: "Not a veteran", 1: "Veteran",98: "Residue"},
    "Citizenship Status": {-1: "Invalid until 2017 Q1", 1: "Born U.S. citizen", 2:"Naturalized citizen", 3: "Non-U.S. Citizen",98: "Residue"},
    "Aggregate Type of Crime": {1: "Violent crime", 2: "Personal theft/larceny"},
    "Type of Crime":{1: "Rape/sexual assault", 2: "Robbery", 3: "Aggravated assault", 4: "Simple assault", 5: "Personal theft/larceny"},
    "Violent Crime Excluding Simple Assault": {1: "Violent crime excluding simple assault", 2: "Simple assault", 3: "Personal theft/larceny"},
    "Series Crime Indicator": {1: "Not a series crime", 2: "Series crime"},
    "Reporting to Police": {1: "Yes", 2: "No", 3: "Do not know", 98: "Residue"},
    "Victim Services": {1: "Yes", 2: "No", 3: "Do not know", 98: "Residue"},
    "Victim-Offender Relationship": {1: "Intimate", 2: "Other relatives", 3: "Well known/casual acquaintance", 4: "Strangers", 5: "Do not know relationship", 6: "Do not know number of offenders"},
    "Presence of Weapon": {1: "Yes", 2: "No", 3: "Do not know if offender had weapon"},
    "Weapon Category": {0: "No weapon", 1: "Firearm", 2: "Knife", 3: "Other type weapon", 4: "Type weapon unknown", 5: "Do not know if offender had weapon"},
    "Location of Crime": {
        1: "At or near victim’s home",
        2: "At or near friend’s, neighbor’s, or relative’s home",
        3: "Commercial place, parking lot, or other public area",
        4: "School",
        5: "Other location",
    },
    "Offender Age": {1: "11 or younger", 2: "12-17", 3: "18-29", 4: "30 or older", 5: "Multiple offenders of various ages", 98: "Residue"},
    "Offender Sex": {1: "Male", 2: "Female", 3: "Both male and female offenders", 4: "Unknown", 98: "Residue"},
    "Offender Race/Hispanic Origin": {
        -1: "Invalid until 2012 Q1",
        1: "Non-Hispanic white",
        2: "Non-Hispanic black",
        3: "Non-Hispanic American Indian/Alaska Native",
        4: "Non-Hispanic Asian/Native Hawaiian/Other Pacific Islander",
        5: "Non-Hispanic more than one race",
        6: "Hispanic",
        7: "Unknown race/Hispanic origin",
        10: "Mixed race group of offenders",
        11: "Unknown number of offenders",
    },
    "Injury": {0: "Not injured", 1: "Injured"},
    "Type of Injury": {1: "No injury", 2: "Serious injury", 3: "Minor injury", 4: "Rape w/o other injuries", 98: "Residue"},
    "Medical Treatment for Injuries": {0: "Not injured", 1: "Not treated", 2: "Treated at scene, home, medical office, or other location", 3: "Do not know", 98: "Residue"},
}

def load_json_files(file_list, data_dir):
    """Load multiple JSON files and return a combined DataFrame."""
    data_frames = []

    for file_name in file_list:
        file_path = os.path.join(data_dir, file_name)
        if not os.path.exists(file_path):
            print(f"Warning: {file_name} not found in {data_dir}")
            continue  # Skip missing files

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and data:  # Ensure it's a non-empty list of records
                    df = pd.DataFrame(data)
                    data_frames.append(df)
                else:
                    print(f"Warning: {file_name} is empty or has an invalid format.")
        except json.JSONDecodeError as e:
            print(f"Error reading {file_name}: {e}")

    return pd.concat(data_frames, ignore_index=True) if data_frames else None


# Process personal dataset
personal_df = load_json_files(PERSONAL_FILES, DATA_DIR)

# Apply descriptive column names and map values
if personal_df is not None:
    personal_df.rename(columns=column_rename_mappings, inplace=True)

    # Extract the quarter and year from "Year and Quarter"
    personal_df["Quarter"] = personal_df["Year and Quarter"].astype(str).str.split(".").str[-1]
    personal_df["Year"] = personal_df["Year and Quarter"].astype(str).str.split(".").str[0]

    # Drop the original "Year and Quarter" column
    personal_df.drop(columns=["Year and Quarter"], inplace=True)

    # Convert categorical columns to integers before mapping
    for column in value_mappings.keys():
        if column in personal_df.columns:
            personal_df[column] = pd.to_numeric(personal_df[column], errors='coerce')

    # Apply value mappings
    for column, mapping in value_mappings.items():
        if column in personal_df.columns:
            personal_df[column] = personal_df[column].map(mapping)

    # Display unique values for verification
    for column in value_mappings.keys():
        if column in personal_df.columns:
            print(f"Unique values in {column} after mapping:", personal_df[column].unique())

    # Reorder columns to place "Quarter" in the third position
    column_order = personal_df.columns.tolist()
    column_order.insert(2, column_order.pop(column_order.index("Quarter")))
    personal_df = personal_df[column_order]

    # Save the cleaned dataset in CSV and TSV formats
    personal_csv_path = os.path.join(OUTPUT_DIR, "ncvs_personal_combined.csv")
    personal_tsv_path = os.path.join(OUTPUT_DIR, "ncvs_personal_combined.tsv")

    personal_df.to_csv(personal_csv_path, index=False)
    personal_df.to_csv(personal_tsv_path, index=False, sep="\t")

    print(f"Personal dataset saved with descriptive names as CSV ({personal_csv_path}) and TSV ({personal_tsv_path}).")
else:
    print("No personal data found. No files were created.")

print("\nData conversion completed successfully!")

#feature engineering
# Define absolute paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")  # Change to "processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure the output directory exists

df = pd.read_csv(os.path.join(DATA_DIR, "ncvs_personal_combined.csv"))

# Transform "type of crime" into separate columns by creating dummy variables
if "Type of Crime" in df.columns:
    crime_dummies = pd.get_dummies(df["Type of Crime"], prefix="", prefix_sep="").groupby(df.index).sum()
    df = pd.concat([df, crime_dummies], axis=1)

    # Define the required crime categories again
    crime_categories = ["Personal theft/larceny", "Robbery", "Simple assault", "Aggravated assault", "Rape/sexual assault"]

    # Check which columns exist
    available_crime_categories = [col for col in crime_categories if col in df.columns]

    if available_crime_categories:
        # Group by 'year', 'quarter', 'offender age', 'offender sex', and 'presence of weapon'
        grouped_df = df.groupby(["Year", "Quarter", "Offender Age", "Offender Sex", "Presence of Weapon"])[available_crime_categories].sum().reset_index()

        # Pivot the data to expand "offender age", "offender sex", and "presence of weapon" into separate columns
        pivoted_df = grouped_df.pivot_table(
            index=["Year", "Quarter"],
            columns=["Offender Age", "Offender Sex", "Presence of Weapon"],
            values=available_crime_categories,
            aggfunc="sum",
            fill_value=0
        )

        # Flatten MultiIndex columns for better readability
        pivoted_df.columns = [f"{col[0]} - {col[1]} - {col[2]} - {col[3]}" for col in pivoted_df.columns]
        pivoted_df.reset_index(inplace=True)

        # Save the processed data as a TSV file
        output_file = os.path.join(OUTPUT_DIR, "ncvs_personal_engineered.tsv")
        pivoted_df.to_csv(output_file, sep="\t", index=False)
    else:
        print("Error: None of the specified crime categories were found in the dataset.")
else:
    print("Error: 'type of crime' column not found in the dataset.")

dtype_mapping = {
    "Person ID": "string",
    "Year": "int32",
    "Quarter": "int8",
    "Age": "string",
    "Sex": "string",
    "Hispanic Origin": "string",
    "Race": "string",
    "Race/Hispanic Origin": "string",
    "Annual Household Income": "string",
    "Annual Household Income (Imputed)": "string",
    "Marital Status": "string",
    "Population Size": "string",
    "Region": "string",
    "Household MSA": "string",
    "Household Locale": "string",
    "Education Level": "string",
    "Education Level (Extended)": "string",
    "Veteran Status": "string",
    "Citizenship Status": "string",
    "Aggregate Type of Crime": "string",
    "Type of Crime": "string",
    "Violent Crime Excluding Simple Assault": "string",
    "Reporting to Police": "string",
    "Victim Services": "string",
    "Location of Crime": "string",
    "Victim-Offender Relationship": "string",
    "Presence of Weapon": "string",
    "Weapon Category": "string",
    "Injury": "string",
    "Type of Injury": "string",
    "Medical Treatment for Injuries": "string",
    "Offender Age": "string",
    "Offender Sex": "string",
    "Offender Race/Hispanic Origin": "string",
    "Victimization Weight": "float32",
    "Series Crime Indicator": "string",
    "Series Adjusted Victimization Weight": "float32",
    "Person Population Weight": "float32",
}

# Load the processed dataset
df = pd.read_csv(os.path.join(DATA_DIR, "ncvs_personal_combined.tsv"), sep="\t", dtype=dtype_mapping, low_memory=False)

# Display the data types of each column
print(df.dtypes)
