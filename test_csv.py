import pandas as pd
import os

print("Current working directory:", os.getcwd())
print()

# Test different paths
csv_paths = ['data/properties.csv', '../data/properties.csv', 'src/data/properties.csv']

for path in csv_paths:
    print(f"Testing path: {path}")
    print(f"File exists: {os.path.exists(path)}")
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            print(f"Successfully read CSV with {len(df)} rows")
            print(f"Columns: {list(df.columns)}")
            print(f"First row: {df.iloc[0].to_dict()}")
        except Exception as e:
            print(f"Error reading CSV: {e}")
    print()
