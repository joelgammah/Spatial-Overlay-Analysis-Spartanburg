import geopandas as gpd
import fiona

# Set the SHAPE_RESTORE_SHX option to YES
fiona.drvsupport.supported_drivers['ESRI Shapefile'] = 'raw'

# Load Census Tracts
census_tracts = gpd.read_file('tl_2019_45_tract.shp')
# Filter for Spartanburg County (using the county FIPS code for Spartanburg County)
spartanburg_tracts = census_tracts[census_tracts['COUNTYFP'] == '083'].copy()

# Load Municipal Boundaries
municipalities = gpd.read_file('tl_2019_45_place.shp')  # Assuming this is the correct file

# Assign a default CRS if none is present
default_crs = "EPSG:4269"  # NAD83

if spartanburg_tracts.crs is None:
    spartanburg_tracts.set_crs(default_crs, inplace=True)

if municipalities.crs is None:
    municipalities.set_crs(default_crs, inplace=True)

# Reproject to NAD83 / UTM Zone 17N
utm_crs = "EPSG:26917"  # NAD83 / UTM zone 17N
spartanburg_tracts = spartanburg_tracts.to_crs(utm_crs)
municipalities = municipalities.to_crs(utm_crs)

# Print the CRS after setting or reprojecting
print("Reprojected Census Tracts CRS:", spartanburg_tracts.crs)
print("Reprojected Municipalities CRS:", municipalities.crs)

# Rename columns to ensure consistency
spartanburg_tracts = spartanburg_tracts.rename(columns={'GEOID': 'tract_id'})
municipalities = municipalities.rename(columns={'GEOID': 'municipality_id'})

# Print column names before calculating areas
print("Spartanburg Tracts Columns Before Area Calculation:", spartanburg_tracts.columns)

# Calculate the total area of each census tract in square meters
spartanburg_tracts['tract_area_sqm'] = spartanburg_tracts.geometry.area

# Print column names after calculating areas
print("Spartanburg Tracts Columns After Area Calculation:", spartanburg_tracts.columns)
print("Spartanburg Tracts with Area:\n", spartanburg_tracts.head())

# Perform spatial overlay analysis to get intersections
intersections = gpd.overlay(spartanburg_tracts, municipalities, how='intersection', keep_geom_type=False)

# Calculate the area of each intersected polygon in square meters
intersections['intersection_area_sqm'] = intersections.geometry.area
print("Intersections:\n", intersections.head())

# Ensure 'tract_id' and 'tract_area_sqm' are included in intersections
intersections = intersections.merge(spartanburg_tracts[['tract_id', 'tract_area_sqm']], on='tract_id', how='left')
print("Intersections with Tract Areas:\n", intersections.head())

# Rename the column after merging to avoid KeyError
if 'tract_area_sqm_y' in intersections.columns:
    intersections = intersections.rename(columns={'tract_area_sqm_y': 'tract_area_sqm'})

# Calculate the proportion for each intersection
intersections['proportion'] = intersections['intersection_area_sqm'] / intersections['tract_area_sqm']

# Summarize the results
summary = intersections.groupby(['tract_id', 'municipality_id']).agg({
    'intersection_area_sqm': 'sum',
    'tract_area_sqm': 'first',
    'proportion': 'sum'
}).reset_index()

# Save the summary to a CSV file
summary.to_csv('spatial_overlay_summary4.csv', index=False)

# Print the summary
print(summary)
