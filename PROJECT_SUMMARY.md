# Manhattan Map Project - Summary

## What We Built

An interactive web-based map of Manhattan featuring three data layers:
1. **Building Layer** - Individual buildings with detailed property data
2. **Census Tract Layer** - Demographic data with 92+ fields
3. **ZIP Code Layer** - ZIP code boundaries

## Key Features

### Interactive Map Controls
- Toggle each layer on/off independently
- Select from 92 different demographic fields to visualize
- Click on any feature (building, census tract, or ZIP code) to see details
- Selected areas highlight in blue
- Color-coded legend for demographic data (yellow to red gradient)
- Works on desktop and mobile (via local network)

### Building Data (42,132 buildings)
Each building marker shows:
- Address
- Year built
- Number of stories
- Total building area (sq ft)
- Lot area (sq ft)
- Land use type (Residential, Commercial, Industrial, etc.)
- Building class code
- Total units and residential units
- Owner type
- Assessed property value

### Census Demographics (1,292 census tracts)
92 demographic fields organized by category:
- **Sex and Age**: Total population, male/female breakdown, age groups, median age
- **Race**: White, Black, Asian, American Indian, Pacific Islander, etc.
- **Hispanic/Latino**: Various Hispanic origins
- **Housing**: Total housing units
- **Voting**: Citizen voting age population

### ZIP Codes (44 Manhattan ZIP codes)
- Light blue polygons showing ZIP code boundaries
- Clickable for ZIP code information

## Technical Stack

### Frontend
- **Leaflet.js** - Interactive mapping library
- **OpenStreetMap** - Base map tiles
- **Leaflet MarkerCluster** - Efficient rendering of 42K+ building markers
- Pure HTML/CSS/JavaScript - No build process needed

### Data Sources
- **NYC PLUTO** (Primary Land Use Tax Lot Output) - Building data
- **U.S. Census Bureau ACS 5-Year Data (2023)** - Demographic data (DP05 Profile)
- **U.S. Census Bureau TIGER/Line** - Census tract boundaries
- **NYC Health Department MODZCTA** - Modified ZIP Code Tabulation Areas

### Data Processing Scripts
1. **extract_manhattan_data.py**
   - Extracts Manhattan buildings from PLUTO CSV
   - Filters ~857K rows to 42K Manhattan buildings with coordinates
   - Outputs: manhattan_buildings.json (14MB)

2. **prepare_census_layer.py**
   - Downloads census tract boundaries from Census Bureau TIGERweb API
   - Reads ACS demographic data from CSV
   - Merges demographic data with tract boundaries
   - Outputs: manhattan_census_tracts.geojson (11MB), census_fields.json (9KB)

3. **prepare_zipcode_layer.py**
   - Downloads NYC ZIP code boundaries from NYC Health GitHub
   - Filters to Manhattan ZIP codes (10001-10282)
   - Outputs: manhattan_zipcodes.geojson (74KB)

## File Structure

```
nymap/
├── manhattan_map.html                    # Main interactive map (17KB)
├── manhattan_buildings.json              # Building data (14MB)
├── manhattan_census_tracts.geojson       # Census tracts + demographics (11MB)
├── manhattan_zipcodes.geojson            # ZIP code boundaries (74KB)
├── census_fields.json                    # Census field metadata (9KB)
├── extract_manhattan_data.py             # Building extraction script
├── prepare_census_layer.py               # Census data preparation script
├── prepare_zipcode_layer.py              # ZIP code preparation script
├── Primary_Land_Use_Tax_Lot_Output_(...).csv  # Source PLUTO data (ignored in git)
├── ACSDP5Y2023.DP05_2025-10-28T231911/   # Source census data (ignored in git)
├── README.md                             # User documentation
└── PROJECT_SUMMARY.md                    # This file
```

## How It Works

### Data Flow
1. **Data Extraction**:
   - Run Python scripts to extract and process data from source files
   - Scripts download geographic boundaries from public APIs
   - Scripts merge demographic data with geographic boundaries
   - Output cleaned JSON/GeoJSON files

2. **Web Serving**:
   - Simple Python HTTP server serves files locally
   - Can be accessed from phone via local network IP

3. **Map Rendering**:
   - Leaflet loads OpenStreetMap base layer
   - Loads three data files asynchronously
   - Renders buildings as clustered markers
   - Renders census tracts as colored polygons
   - Renders ZIP codes as outlined polygons
   - User interactions update layers and highlights

### Key Implementation Details

**Performance Optimizations**:
- Marker clustering for 42K buildings (prevents browser slowdown)
- Chunked loading for smooth interaction
- GeoJSON for efficient vector data storage
- Lazy loading - only active layers consume resources

**User Experience**:
- Click highlighting with blue borders
- Separate toggle controls for each layer
- Dynamic legend that updates with field selection
- Formatted numbers (commas, currency)
- Human-readable labels (land use decoded from codes)
- Responsive popups with comprehensive information

## Usage

### Local Development
```bash
# Start web server
python -m http.server 8000

# Access on computer
open http://localhost:8000/manhattan_map.html

# Access on phone (same WiFi)
# http://<your-local-ip>:8000/manhattan_map.html
```

### Deployment to GitHub Pages
1. Create new GitHub repository
2. Push files (excluding large CSV sources)
3. Enable GitHub Pages in repo settings
4. Access at: `https://username.github.io/repo-name/manhattan_map.html`

## Future Enhancement Ideas

- Add more census data tables (economic, housing, etc.)
- Aggregate building metrics by census tract
- Filter buildings by criteria (year, size, type)
- Search functionality for addresses
- Export selected data to CSV
- Time-series visualization (if historical data added)
- 3D building visualization using height data
- Compare demographics across tracts
- Custom color schemes for choropleth maps

## Credits

Built with Claude Code as an interactive data visualization project combining NYC open data sources with U.S. Census demographics.
