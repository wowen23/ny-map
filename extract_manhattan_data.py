import csv
import json

# Read the CSV and extract Manhattan buildings
manhattan_buildings = []

with open('Primary_Land_Use_Tax_Lot_Output_(PLUTO)_20251028.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        # Filter for Manhattan only
        if row['borough'] == 'MN':
            # Only include buildings with valid coordinates and at least some data
            if row['latitude'] and row['longitude']:
                building = {
                    'address': row['address'],
                    'yearbuilt': row['yearbuilt'] if row['yearbuilt'] else 'Unknown',
                    'numfloors': row['numfloors'] if row['numfloors'] else 'Unknown',
                    'lat': float(row['latitude']),
                    'lon': float(row['longitude'])
                }
                manhattan_buildings.append(building)

print(f"Extracted {len(manhattan_buildings)} Manhattan buildings with coordinates")

# Save to JSON
with open('manhattan_buildings.json', 'w', encoding='utf-8') as f:
    json.dump(manhattan_buildings, f, indent=2)

print("Data saved to manhattan_buildings.json")
