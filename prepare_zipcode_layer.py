import requests
import json

print("Downloading NYC ZIP Code boundaries...")

# Use NYC Planning MODZCTA (Modified ZCTA) from their GitHub
# This is a public GeoJSON file
url = "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/Geography-resources/MODZCTA_2010_WGS1984.geo.json"
params = {}

response = requests.get(url, params=params)
if response.status_code == 200:
    all_zipcodes = response.json()

    # Debug: check response structure
    if 'features' not in all_zipcodes:
        print("Response structure:", list(all_zipcodes.keys())[:10])
        print("First part of response:", str(all_zipcodes)[:500])
        exit(1)

    print(f"Downloaded {len(all_zipcodes['features'])} ZIP codes for NYC")
else:
    print(f"Error downloading: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    exit(1)

# Debug: Check what fields are available
if len(all_zipcodes['features']) > 0:
    print("Sample properties:", all_zipcodes['features'][0]['properties'])

# Filter for Manhattan ZIP codes (100xx-102xx range)
manhattan_zips = []
for feature in all_zipcodes['features']:
    props = feature['properties']

    # Try different field names
    zipcode = props.get('MODZCTA', props.get('zipcode', props.get('ZIPCODE', props.get('modzcta', props.get('label', '')))))

    if zipcode:
        # Clean up zipcode string
        zipcode = str(zipcode).strip()
        try:
            zip_num = int(zipcode)
            # Manhattan ZIP codes are roughly 10001-10282
            if 10001 <= zip_num <= 10282:
                manhattan_zips.append(feature)
        except ValueError:
            # Might be a string like "10001" or "NA"
            if zipcode.isdigit():
                zip_num = int(zipcode)
                if 10001 <= zip_num <= 10282:
                    manhattan_zips.append(feature)

print(f"Filtered to {len(manhattan_zips)} Manhattan ZIP codes")

# Create GeoJSON output
output = {
    "type": "FeatureCollection",
    "features": manhattan_zips
}

# Save to file
with open('manhattan_zipcodes.geojson', 'w') as f:
    json.dump(output, f)

print(f"Saved {len(manhattan_zips)} Manhattan ZIP codes to manhattan_zipcodes.geojson")

# Print list of ZIP codes found
zipcodes_list = sorted([f['properties'].get('MODZCTA', '')
                        for f in manhattan_zips if f['properties'].get('MODZCTA')])
print(f"\nZIP codes found ({len(zipcodes_list)}): {', '.join(map(str, zipcodes_list))}")
