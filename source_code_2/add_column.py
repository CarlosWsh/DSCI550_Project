import pandas as pd

# read the tsv file
df = pd.read_csv('/Users/carlos/Documents/GitHub/DSCI550_Project/data_2/hp_analysis_hw2.tsv', sep='\t')

# Add new columns with default empty values
df["GeoTopicName"] = ""
df["GeoTopicLat"] = ""
df["GeoTopicLng"] = ""
df["NER_Entities"] = ""
df["Image_File"] = ""
df["Image_Caption"] = ""
df["Image_Objects"] = ""

# Save the updated DataFrame to a new TSV file
df.to_csv('/Users/carlos/Documents/GitHub/DSCI550_Project/data_2/hp_analysis_hw2.tsv', sep='\t', index=False)
