# Manhattan Buildings & Demographics Map

An interactive OpenStreetMap visualization of Manhattan with two data layers:

## Features

### Building Layer
- 42,132 Manhattan buildings with detailed PLUTO data:
  - Building address
  - Year built
  - Number of stories
  - Total building area (sq ft)
  - Lot area (sq ft)
  - Land use type (Residential, Commercial, etc.)
  - Building class code
  - Total units
  - Residential units
  - Owner type
  - Assessed value

### Census Demographics Layer
- 1,292 census tracts with 92 demographic fields including:
  - Population by age groups
  - Race and ethnicity statistics
  - Gender demographics
  - And more...

### ZIP Code Layer
- 44 Manhattan ZIP codes with boundaries
- Click to see ZIP code details

## Usage

Open `manhattan_map.html` in your browser or visit the GitHub Pages site.

**Controls:**
- Toggle building markers on/off
- Toggle census tract polygons on/off
- Toggle ZIP code boundaries on/off
- Select different demographic fields to visualize census data
- Click on buildings, census tracts, or ZIP codes for detailed info
- Selected areas are highlighted in blue
- Color-coded legend shows census data distribution

## Data Sources

- **Buildings**: NYC PLUTO (Primary Land Use Tax Lot Output) dataset
- **Census Data**: American Community Survey 5-Year Data (2023) - DP05 Demographic Profile
- **Census Boundaries**: U.S. Census Bureau TIGER/Line Shapefiles
- **ZIP Code Boundaries**: NYC Health Department MODZCTA (Modified ZIP Code Tabulation Areas)

## Files

- `manhattan_map.html` - Interactive map viewer
- `manhattan_buildings.json` - Building data with PLUTO details (42,132 buildings, 14MB)
- `manhattan_census_tracts.geojson` - Census tracts with demographics (1,292 tracts, 11MB)
- `manhattan_zipcodes.geojson` - ZIP code boundaries (44 ZIP codes, 74KB)
- `census_fields.json` - Field definitions for census data
- `extract_manhattan_data.py` - Script to extract building data from PLUTO CSV
- `prepare_census_layer.py` - Script to download and merge census data with boundaries
- `prepare_zipcode_layer.py` - Script to download ZIP code boundaries
