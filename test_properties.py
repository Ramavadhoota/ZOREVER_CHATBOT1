import pandas as pd
import os

# Load the CSV file
csv_path = 'data/properties.csv'
df = pd.read_csv(csv_path)

print("=== PROPERTY DATA TEST ===")
print(f"Total properties: {len(df)}")
print(f"Columns: {list(df.columns)}")
print()

print("=== PROPERTY IDs ===")
for _, row in df.iterrows():
    print(f"ID: {row['listing_id']} - {row['property_name']}")
print()

print("=== SEARCH TEST ===")
# Test property ID search
test_id = "P003"
print(f"Searching for ID: {test_id}")
result = df[df['listing_id'] == test_id]
print(f"Found: {len(result)} matches")
if len(result) > 0:
    print(f"Property: {result.iloc[0]['property_name']}")
print()

# Test property name search
test_name = "Sunrise Apartments"
print(f"Searching for name: {test_name}")
result = df[df['property_name'].str.contains(test_name, case=False)]
print(f"Found: {len(result)} matches")
if len(result) > 0:
    print(f"Property: {result.iloc[0]['property_name']}")
print()

print("=== ALL PROPERTIES ===")
for _, row in df.iterrows():
    print(f"{row['listing_id']}: {row['property_name']} - {row['city']} - ${row['price']:,}")
