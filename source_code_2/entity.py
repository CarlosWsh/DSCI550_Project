import pandas as pd
import spacy
import en_core_web_sm
from collections import Counter

# Load the TSV file
df = pd.read_csv('/Users/carlos/Documents/GitHub/DSCI550_Project/data_2/hp_analysis_hw2.tsv', sep='\t')

# Load the English NLP model
nlp = en_core_web_sm.load()

# Initialize result columns
entities_list = []
entity_labels_list = []
entity_counts_list = []

# Adjust this column name based on your dataset
description_column = "description"  # or change to the correct column name

# Process each row
for desc in df[description_column].astype(str):
    doc = nlp(desc)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    entity_texts = [ent[0] for ent in entities]
    entity_labels = [ent[1] for ent in entities]
    entity_count = dict(Counter(entity_labels))

    entities_list.append(", ".join(entity_texts))
    entity_labels_list.append(", ".join(entity_labels))
    entity_counts_list.append(str(entity_count))

# Add new columns to your DataFrame
df["entities"] = entities_list
df["entity_labels"] = entity_labels_list
df["entity_counts"] = entity_counts_list

# Save the updated TSV
df.to_csv('/Users/carlos/Documents/GitHub/DSCI550_Project/data_2/hp_analysis_with_entities.tsv', sep='\t', index=False)
