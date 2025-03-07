import pandas as pd
import os
from transformers import pipeline

# Define paths dynamically
data_dir = os.path.join("..", "data")
raw_dir = os.path.join(data_dir, "raw")
processed_dir = os.path.join(data_dir, "processed")

# Ensure the processed directory exists
os.makedirs(processed_dir, exist_ok=True)

# Define file paths
input_file = os.path.join(raw_dir, "haunted_places.csv")
output_file = os.path.join(processed_dir, "hp_with_date_and_witness_count.csv")

# Load CSV
hp_df = pd.read_csv(input_file)

# Initialize AI model
pipe = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct", device_map="auto")


def date_extraction(description):
    prompt = """
        The text below is a description of a haunted location.\n
        Please extract out the date that the haunted location is dated to with the format: Month-Day-Year\n
        If no date is mentioned, then put 'N/A' as your output.\n
        If part of the date is mentioned, put the dates available with 00 as filler for the other values.\n
        Please output your final result after: #### 

        For example:\n
        Description: "The house dated back to the 20th century", output: #### 01-01-1900\n
        Description: "The location was discovered in May of 1854", output: #### 05-01-1854\n
        Description: "If you take the road towards the beach, you will come to a gravel road leading north", output: #### N/A\n
        \n\n
        Description:\n
    """
    messages = [{"role": "user", "content": prompt + description}]

    try:
        llama_output = pipe(messages)[0]['generated_text'][1]['content']
        final_date = llama_output.split("####")[-1].strip()
    except Exception as e:
        print(f"Error extracting date: {e}")
        final_date = "N/A"

    return final_date


def witness_count_extraction(description):
    prompt = """
        The text below is a description of a haunted location.\n
        Please extract out the witness count from the haunted location.\n
        If no witness count is mentioned, then put 'N/A' as your output.\n
        Please output your final result after: #### 

        For example:\n
        Description: "A mysterious figure was seen by 3 eye witnesses", output: #### 3\n
        Description: "People said they heard voices", output: #### N/A\n
        \n\n
        Description:\n
    """
    messages = [{"role": "user", "content": prompt + description}]

    try:
        llama_output = pipe(messages)[0]['generated_text'][1]['content']
        final_witness_count = llama_output.split("####")[-1].strip()
    except Exception as e:
        print(f"Error extracting witness count: {e}")
        final_witness_count = "N/A"

    return final_witness_count


# Processing each row and adding extracted values
haunted_place_date_list = []
witness_count_list = []

for index, row in hp_df.iterrows():
    if index % 10 == 0:  # Print progress every 10 rows
        print(f"Processing row {index}/{len(hp_df)}")

    date = date_extraction(row['description'])
    witness_count = witness_count_extraction(row['description'])

    haunted_place_date_list.append(date)
    witness_count_list.append(witness_count)

# Add extracted data to DataFrame
hp_df['HP_date'] = haunted_place_date_list
hp_df['Witness_count'] = witness_count_list

# Save to processed directory
hp_df.to_csv(output_file, index=False)
print(f"File saved successfully: {output_file}")
