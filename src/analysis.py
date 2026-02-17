import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIGURATION ---
# Make sure your file in the data folder is named exactly this:
DATA_FILE = 'data/survey_data.xlsx' 
OUTPUT_FOLDER = 'outputs'

# --- 1. LOAD DATA ---
if not os.path.exists(DATA_FILE):
    print(f"ERROR: The file '{DATA_FILE}' was not found.")
    print("Files in data directory:")
    if os.path.exists('data'):
        print(os.listdir('data'))
    else:
        print("'data' directory missing.")
    exit(1)

try:
    # UPDATED: Use read_excel for .xlsx files
    # We skip rows 2 and 3 (index 1 and 2) to match the header format
    df = pd.read_excel(DATA_FILE, engine='openpyxl', skiprows=[1, 2])
    print("Successfully loaded Excel file.")
    
except Exception as e:
    print(f"Failed to read Excel file: {e}")
    exit(1)

# --- 2. MAP COLUMNS TO COURSE NAMES ---
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
# Check if columns exist before proceeding
missing_cols = [col for col in course_mapping.keys() if col not in df.columns]
if missing_cols:
    print(f"ERROR: Could not find columns: {missing_cols}")
    print("Columns found in file:", df.columns.tolist()[:10])
    exit(1)

df_clean = df[list(course_mapping.keys())].copy()
df_clean.rename(columns=course_mapping, inplace=True)

# "Melt" the data
df_melted = df_clean.melt(var_name='Course', value_name='Rank')
df_melted.dropna(inplace=True)
df_melted['Rank'] = pd.to_numeric(df_melted['Rank'])

# --- 4. GENERATE RANKING ---
ranking_summary = df_melted.groupby('Course')['Rank'].mean().sort_values()
print("Rank Order (Lower is Better):")
print(ranking_summary)

# --- 5. CREATE FIGURE ---
plt.figure(figsize=(10, 6))
sns.barplot(x=ranking_summary.values, y=ranking_summary.index, palette='viridis')
plt.xlabel('Average Rank (1 = Most Beneficial)')
plt.title('MAcc Core Course Student Rankings')
plt.tight_layout()

# --- 6. SAVE OUTPUT ---
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
output_path = os.path.join(OUTPUT_FOLDER, 'rank_order.png')
plt.savefig(output_path)
print(f"Chart saved to {output_path}")
