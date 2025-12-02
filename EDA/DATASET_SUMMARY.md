# Delhivery Dataset Summary

## Download Information
- **File Name:** delhivery_data.csv
- **File Size:** 55,617,130 bytes (~53 MB)
- **Downloaded:** December 1, 2025, 07:27:01
- **Source:** https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/001/551/original/delhivery_data.csv?1642751181

## Dataset Overview

### Shape
- **Rows:** 144,867 records
- **Columns:** 24 features

### Column List
1. data
2. trip_creation_time
3. route_schedule_uuid
4. route_type
5. trip_uuid
6. source_center
7. source_name
8. destination_center
9. destination_name
10. od_start_time
11. od_end_time
12. start_scan_to_end_scan
13. is_cutoff
14. cutoff_factor
15. cutoff_timestamp
16. actual_distance_to_destination
17. actual_time
18. osrm_time
19. osrm_distance
20. factor
21. segment_actual_time
22. segment_osrm_time
23. segment_osrm_distance
24. segment_factor

## Data Types

### Object (String) Columns (11)
- data
- trip_creation_time
- route_schedule_uuid
- route_type
- trip_uuid
- source_center
- source_name
- destination_center
- destination_name
- od_start_time
- od_end_time
- cutoff_timestamp

### Numeric Columns (12)
- start_scan_to_end_scan (float64)
- cutoff_factor (int64)
- actual_distance_to_destination (float64)
- actual_time (float64)
- osrm_time (float64)
- osrm_distance (float64)
- factor (float64)
- segment_actual_time (float64)
- segment_osrm_time (float64)
- segment_osrm_distance (float64)
- segment_factor (float64)

### Boolean Columns (1)
- is_cutoff (bool)

## Missing Values Analysis

### Columns with Missing Values
- **source_name:** 293 missing values (0.20%)
- **destination_name:** 261 missing values (0.18%)

### Columns with No Missing Values
All other 22 columns have complete data (0 missing values)

## Key Observations

1. **Data Quality:** Very good - only 2 columns have missing values, and the percentage is minimal (<0.2%)

2. **Time Columns:** Multiple time-related columns need to be converted to datetime format:
   - trip_creation_time
   - od_start_time
   - od_end_time
   - cutoff_timestamp

3. **Categorical Features:**
   - data (training/testing indicator)
   - route_type (FTL/Carting)
   - Various location identifiers

4. **Numeric Features:** Rich set of distance and time metrics for both actual and OSRM (routing engine) calculations

5. **Segmented Data:** The dataset contains segment-level information that needs to be aggregated at trip level

## Next Steps for Analysis

1. ✅ **Data Cleaning**
   - Handle 293 missing values in source_name
   - Handle 261 missing values in destination_name
   - Convert time columns to datetime format

2. ✅ **Feature Engineering**
   - Create segment_key (trip_uuid + source_center + destination_center)
   - Extract features from source_name and destination_name
   - Calculate time differences
   - Extract date components from trip_creation_time

3. ✅ **Data Aggregation**
   - Aggregate at segment level
   - Aggregate at trip level
   - Apply appropriate aggregation functions

4. ✅ **Analysis**
   - Outlier detection and treatment
   - Hypothesis testing (actual vs OSRM metrics)
   - Business insights generation

## File Location
`C:\Users\rattu\Downloads\Delhivery\delhivery_data.csv`
