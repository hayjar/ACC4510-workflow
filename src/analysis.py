import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIGURATION ---
# We assume the file is inside a 'data' folder.
DATA_FILE = 'data/survey_data.csv' 
OUTPUT_FOLDER = 'outputs'

# --- 1. LOAD DATA ---
# The file has 3 header rows. We keep the first one (index 0) and skip rows 2 and 3 (index 1 and 2).
# This gives us headers like 'Q35_1', 'Q35_5', etc.
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Could not find {DATA_FILE}. Make sure the file is in the 'data' folder.")

df = pd.read_csv(DATA_FILE, skiprows=[1, 2])

# --- 2. MAP COLUMNS TO COURSE NAMES ---
# Mapping based on the specific Question IDs in your dataset
course_mapping = {
    'Q35_1': 'ACC 6060: Pro. & Leadership',
    'Q35_5': 'ACC 6300: Data Analytics',
    'Q35_2': 'ACC 6400: Adv. Tax Entities',
    'Q35_4': 'ACC 6510: Financial Audit',
    'Q35_3': 'ACC 6540: Pro. Ethics',
    'Q35_8': 'ACC 6560: Fin. Theory I',
    'Q35_9': 'ACC 6350: Mgmt Control Sys',
    'Q35_10': 'ACC 6600: Business Law'
}

# --- 3. CLEAN AND RESHAPE ---
# Filter only the columns we need
df_clean = df[list(course_mapping.keys())].copy()

# Rename them to readable course names
df_clean.rename(columns=course_mapping, inplace=True)

# "Melt" the data (unpivot) so we have one row per ranking
df_melted = df_clean.melt(var_name='Course', value_name='Rank')

# Remove empty rankings and ensure numbers are integers
df_melted.dropna(inplace=True)
df_melted['Rank'] = pd.to_numeric(df_melted['Rank'])

# --- 4. GENERATE RANKING ---
# Calculate average rank (Lower number = Better rank)
ranking_summary = df_melted.groupby('Course')['Rank'].mean().sort_values()
print("Rank Order (Lower is Better):")
print(ranking_summary)

# --- 5. CREATE FIGURE ---
plt.figure(figsize=(10, 6))
# Create a bar chart
sns.barplot(x=ranking_summary.values, y=ranking_summary.index, palette='viridis')
plt.xlabel('Average Rank (1 = Most Beneficial)')
plt.title('MAcc Core Course Student Rankings')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()

# --- 6. SAVE OUTPUT ---
# Create the outputs folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
output_path = os.path.join(OUTPUT_FOLDER, 'rank_order.png')
plt.savefig(output_path)
print(f"Chart saved to {output_path}")
