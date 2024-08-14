
# Spatial Overlay Analysis of Municipalities in Spartanburg County

## Overview
This project performs a spatial overlay analysis for the municipalities in Spartanburg County. The goal of the analysis is to determine the proportion of each census tract that falls within each municipality. This involves calculating the area of overlap between census tracts and municipal boundaries.

For each census tract that overlaps multiple municipalities, the analysis calculates the weight based on the area of overlap. For example, if 60% of a census tract falls within Municipality A and 40% falls within Municipality B, the weights will be 0.6 and 0.4, respectively.

## Files
- `soc.py`: The Python script that conducts the spatial overlay analysis.
- `spatial_overlay_summary4.csv`: The summary of the spatial overlay analysis results.

## How to Run
1. Ensure you have Python and the necessary libraries installed.
2. Run the `soc.py` script to perform the analysis.
3. The results are saved in the `spatial_overlay_summary4.csv` file.

## Dependencies
- Python 3.x
- `geopandas` library for handling spatial data
- `pandas` library for data manipulation

## Analysis Methodology
1. **Data Preparation**: The municipal boundaries and census tracts are loaded using `geopandas` and projected to a suitable coordinate reference system for area calculation.
2. **Spatial Overlay**: The analysis performs a spatial intersection between the census tracts and municipalities to determine the overlapping areas.
3. **Area Calculation**: The area of each overlapping region is calculated, and the proportion of each census tract that falls within each municipality is determined.
4. **Weight Calculation**: For census tracts that overlap multiple municipalities, the weight of each municipality is calculated based on the proportion of the area within the tract.

## Results
The results of the spatial overlay analysis provide insights into the spatial relationships between different municipalities and census tracts in Spartanburg County. The output is a CSV file summarizing the proportion of each census tract that falls within each municipality.




