# Delhivery Feature Engineering - Solution Approach Memory

## Project Overview
**Topic:** Feature Engineering  
**Duration:** 1 week  
**Company:** Delhivery - India's leading integrated logistics player

## Business Context

### Company Objective
Delhivery aims to create a commerce operating system by:
- Utilizing world-class infrastructure
- Ensuring highest quality logistics operations
- Harnessing cutting-edge engineering and technology capabilities

### Case Study Purpose

**From Delhivery's Perspective:**
- Establish itself as the premier player in the logistics industry
- Ensure data integrity and quality
- Extract valuable features from raw data for forecasting models
- Identify patterns, insights, and actionable recommendations
- Optimize logistics operations through hypothesis testing and outlier detection

**From Learners' Perspective:**
- Hands-on experience in data preprocessing and cleaning
- Feature engineering for machine learning models
- Data grouping and aggregation techniques
- Hypothesis testing and validation
- Deriving actionable business insights

## Dataset Information

### Data Source
URL: `https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/001/551/original/delhivery_data.csv?1642751181`

### Column Profiling (24 columns)

1. **data** - Testing or training data indicator
2. **trip_creation_time** - Timestamp of trip creation
3. **route_schedule_uuid** - Unique ID for route schedule
4. **route_type** - Transportation type:
   - FTL (Full Truck Load): Direct delivery, no other pickups/drop-offs
   - Carting: Small vehicles handling system
5. **trip_uuid** - Unique trip identifier (may include multiple source/destination centers)
6. **source_center** - Source ID of trip origin
7. **source_name** - Source name of trip origin
8. **destination_center** - Destination ID
9. **destination_name** - Destination name
10. **od_start_time** - Trip start time
11. **od_end_time** - Trip end time
12. **start_scan_to_end_scan** - Time taken from source to destination
13. **is_cutoff** - Unknown field
14. **cutoff_factor** - Unknown field
15. **cutoff_timestamp** - Unknown field
16. **actual_distance_to_destination** - Distance in km between source and destination
17. **actual_time** - Actual delivery time (Cumulative)
18. **osrm_time** - Open-source routing engine time (Cumulative, includes traffic and road types)
19. **osrm_distance** - Open-source routing engine distance (Cumulative)
20. **factor** - Unknown field
21. **segment_actual_time** - Segment time for package subset
22. **segment_osrm_time** - OSRM segment time for package subset
23. **segment_osrm_distance** - OSRM distance for package subset
24. **segment_factor** - Unknown field

### Key Data Characteristics
- Delivery details of one package are divided into multiple rows (like connecting flights)
- Data represents segments of trips that need to be aggregated
- Contains both actual and OSRM (routing engine) metrics for comparison

## Solution Approach

### 1. Basic Data Cleaning and Exploration
- Handle missing values
- Convert time columns to pandas datetime
- Analyze dataset structure and characteristics

### 2. Data Merging Strategy

#### A. Grouping by Segment
**Create segment_key:**
- Unique identifier combining: `trip_uuid + source_center + destination_center`

**Aggregate segment metrics:**
- Use `groupby` and `cumsum()` to merge rows
- Create new columns:
  - `segment_actual_time_sum`
  - `segment_osrm_distance_sum`
  - `segment_osrm_time_sum`

#### B. Aggregating at Segment Level
**Steps:**
1. Create `create_segment_dict` defining aggregation rules
2. Keep first/last values for fields where aggregation doesn't make sense
3. Group by `segment_key`
4. Apply aggregation functions
5. Sort by:
   - `segment_key` (for consistency)
   - `od_end_time` (ascending, earliest to latest)

### 3. Feature Engineering

**Extract features from:**

1. **Time Difference:**
   - Calculate `od_time_diff_hour` = od_end_time - od_start_time
   - Drop original columns if required

2. **Destination Name:**
   - Split format: City-place-code (State)
   - Extract: City, Place, Code, State

3. **Source Name:**
   - Split format: City-place-code (State)
   - Extract: City, Place, Code, State

4. **Trip Creation Time:**
   - Extract: month, year, day, hour, day_of_week, etc.

### 4. In-Depth Analysis

#### A. Trip-Level Aggregation
- Group segment data by `trip_uuid`
- Apply aggregation functions (first, last, sum) from `create_trip_dict`
- Calculate summary statistics for each trip

#### B. Outlier Detection & Treatment
- Find outliers in numerical features
- Visualize using Boxplot
- Handle outliers using IQR method

#### C. Encoding & Scaling
- One-hot encoding for categorical features
- Normalize/Standardize numerical features using:
  - MinMaxScaler, or
  - StandardScaler

### 5. Hypothesis Testing

**Perform hypothesis testing/visual analysis between:**

1. Actual time (aggregated) vs OSRM time (aggregated)
2. Actual time (aggregated) vs Segment actual time (aggregated)
3. OSRM distance (aggregated) vs Segment OSRM distance (aggregated)
4. OSRM time (aggregated) vs Segment OSRM time (aggregated)

**Note:** Aggregated values are obtained after merging rows based on `trip_uuid`

### 6. Business Insights & Recommendations

**Pattern Analysis:**
- Identify where most orders originate (State, Corridor, etc.)
- Determine busiest corridors
- Calculate average distance between corridors
- Calculate average time taken per corridor

**Actionable Items:**
- Provide data-driven recommendations for business optimization
- Identify operational bottlenecks
- Suggest resource allocation improvements

## Key Considerations

### Data Merging Logic
When combining rows representing segments of the same trip:
- **Numeric fields:** Use appropriate aggregation (sum, mean, first, last)
- **Categorical fields:** Keep first or last value
- **Time fields:** Consider start of first segment and end of last segment

### Aggregation Strategy
- **Segment level:** Combine consecutive segments of a trip
- **Trip level:** Aggregate all segments belonging to same trip_uuid
- Maintain temporal ordering (od_end_time)

### Unknown Fields
Fields like `is_cutoff`, `cutoff_factor`, `cutoff_timestamp`, `factor`, and `segment_factor` are marked as unknown - may require domain expertise or can be dropped if not useful

## Expected Deliverables

1. **Cleaned Dataset:** Properly structured with handled missing values
2. **Engineered Features:** Extracted from raw fields
3. **Aggregated Data:** At segment and trip levels
4. **Statistical Analysis:** Hypothesis testing results
5. **Visualizations:** Boxplots, distribution plots, comparison charts
6. **Business Insights:** Patterns and actionable recommendations
7. **Documentation:** Jupyter notebook with clear explanations

## Submission Guidelines

- Convert Jupyter notebook to PDF
- Upload to Google Drive with public access
- Include insights and recommendations
- Optional: Add images/graphs via screenshots or plt.savefig()
- No editing allowed after submission

## Technical Stack

- **Platform:** Google Colab or Jupyter Notebook
- **Language:** Python
- **Libraries:** pandas, numpy, matplotlib, seaborn, scipy (for hypothesis testing)
- **Techniques:** GroupBy, Aggregation, Feature Engineering, Outlier Detection, Hypothesis Testing

## Success Criteria

- Proper data cleaning and handling of missing values
- Successful merging of segmented trip data
- Meaningful feature extraction
- Valid hypothesis testing
- Actionable business insights
- Clear documentation and visualization

---

**Note:** This is a learning-focused case study with lenient evaluation. The goal is to develop skills in dealing with business uncertainty and deriving insights from complex, real-world logistics data.
