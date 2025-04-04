import pandas as pd

# Load the TSV file
df = pd.read_csv('/Users/carlos/Documents/GitHub/DSCI550_Project/data_2/hp_analysis_hw2.tsv', sep='\t')

# Caption generator
def create_caption(row):
    location = row.get("location")
    description = row.get("description")
    state = row.get("state", "")

    if pd.notnull(location) and pd.notnull(description):
        return f"An eerie illustration of {location}" + \
               (f" in {state}" if pd.notnull(state) and state else "") + \
               f" — {description.strip()}"
    else:
        return "unset"

df["Image_Caption"] = df.apply(create_caption, axis=1)
# Save updated TSV
df.to_csv('/Users/carlos/Documents/GitHub/DSCI550_Project/data_2/hp_analysis_hw2.tsv', sep='\t', index=False)

##########