import requests
import json
import csv

print("Downloading NYC census tract boundaries...")

# Try Census Bureau's TIGERweb service for NY County (Manhattan) - FIPS 36061
# Using the 2020 census tracts
url = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2021/MapServer/8/query"
params = {
    'where': "STATE='36' AND COUNTY='061'",  # New York State, New York County (Manhattan)
    'outFields': '*',
    'f': 'geojson'
}

response = requests.get(url, params=params)
if response.status_code == 200:
    census_tracts = response.json()
    print(f"Downloaded {len(census_tracts['features'])} census tracts")
else:
    print(f"Error downloading: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    exit(1)

# Read census data
print("Reading census demographic data...")
census_data = {}

with open('ACSDP5Y2023.DP05_2025-10-28T231911/ACSDP5Y2023.DP05-Data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    next(reader)  # Skip the label row

    for row in reader:
        # Extract tract ID from GEO_ID (format: 1400000US36061XXXXXX)
        geo_id = row['GEO_ID']
        if geo_id.startswith('1400000US36061'):  # Manhattan only
            # Extract last 6 digits as tract code
            tract_code = geo_id[-6:]
            # Remove leading zeros for matching
            tract_code_clean = tract_code.lstrip('0') or '0'
            census_data[tract_code] = row
            census_data[tract_code_clean] = row

print(f"Loaded demographic data for {len(census_data)} census tracts")

# Read column metadata for better field names
print("Reading column metadata...")
field_metadata = {}
with open('ACSDP5Y2023.DP05_2025-10-28T231911/ACSDP5Y2023.DP05-Column-Metadata.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        field_metadata[row['Column Name']] = row['Label']

# Filter Manhattan census tracts and merge with demographic data
manhattan_tracts = []
matched = 0
unmatched = 0

for feature in census_tracts['features']:
    props = feature['properties']

    # Get tract code from properties - try different field names
    tract = props.get('TRACT', props.get('TRACTCE', props.get('GEOID', props.get('tract', ''))))

    if tract:
        # Try various formats
        tract_str = str(tract)
        tract_variants = [
            tract_str,
            tract_str.lstrip('0') or '0',
            tract_str.zfill(6),
        ]

        census_row = None
        for variant in tract_variants:
            if variant in census_data:
                census_row = census_data[variant]
                matched += 1
                break

        if census_row:
            # Add demographic data to properties
            feature['properties']['census_data'] = census_row
            manhattan_tracts.append(feature)
        else:
            # Add tract without demographic data
            feature['properties']['census_data'] = None
            manhattan_tracts.append(feature)
            unmatched += 1
    else:
        # Add tract without data
        manhattan_tracts.append(feature)
        unmatched += 1

print(f"Matched {matched} tracts with demographic data")
print(f"Unmatched {unmatched} tracts")

# Create GeoJSON with Manhattan tracts
output = {
    "type": "FeatureCollection",
    "features": manhattan_tracts
}

# Save to file
with open('manhattan_census_tracts.geojson', 'w') as f:
    json.dump(output, f)

print(f"Saved {len(manhattan_tracts)} Manhattan census tracts to manhattan_census_tracts.geojson")

# Save field metadata for the frontend
interesting_fields = {}
for col, label in field_metadata.items():
    if col.endswith('E') and not col.endswith('PE'):  # Estimates only, not percentages
        if any(keyword in label for keyword in ['Total population', 'Male', 'Female', 'Median age',
                                                  'Under 18', '65 years and over', 'White', 'Black',
                                                  'Asian', 'Hispanic', 'race']):
            interesting_fields[col] = label

with open('census_fields.json', 'w') as f:
    json.dump(interesting_fields, f, indent=2)

print(f"Saved {len(interesting_fields)} field definitions to census_fields.json")
