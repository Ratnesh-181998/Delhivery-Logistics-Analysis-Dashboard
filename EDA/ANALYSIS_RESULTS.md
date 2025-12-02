# Delhivery Feature Engineering - Analysis Results

## 1. Dataset Overview
- **Shape:** 144,867 rows, 24 columns
- **Data Period:** September - October 2018
- **Key Features:** Trip timestamps, source/destination info, routing metrics (OSRM vs Actual)

## 2. Hypothesis Testing Results

We performed Kolmogorov-Smirnov (KS) tests to compare the distributions of various time metrics.

| Comparison | Statistic | P-Value | Result | Interpretation |
|------------|-----------|---------|--------|----------------|
| **Time Taken (OD) vs Start Scan to End Scan** | 0.0030 | 1.0000 | **SIMILAR** | The total trip duration calculated from timestamps matches the scan duration. |
| **Actual Time vs Start Scan to End Scan** | 0.5295 | 0.0000 | **DIFFERENT** | Actual delivery time is significantly different from the scan duration. |
| **Actual Time vs OSRM Time** | 0.2945 | 0.0000 | **DIFFERENT** | Actual time taken is significantly different from the estimated OSRM time. |
| **Actual Time vs Segment Actual Time** | 0.0086 | 0.6348 | **SIMILAR** | Aggregated segment times match the total actual time (data consistency check passed). |
| **OSRM Time vs Segment OSRM Time** | 0.0351 | 0.0000 | **DIFFERENT** | Aggregated OSRM segment times differ from the total OSRM trip time. |

### Key Findings:
1. **OSRM Discrepancy:** There is a significant difference between the OSRM (routing engine) estimated time and the actual time taken. This suggests the routing engine might need calibration or that real-world factors (traffic, breaks) are significantly impacting delivery times.
2. **Data Consistency:** The match between `Actual Time` and `Segment Actual Time` confirms that the segment-level data aggregates correctly to the trip-level totals.
3. **Scan vs Actual:** The difference between `Actual Time` and `Start Scan to End Scan` suggests that "Actual Time" might include non-driving time or processing time that isn't captured in the scan duration, or vice versa.

## 3. Business Insights

### Busiest Corridors (State-to-State)
The majority of trips are **intra-state** (within the same state), indicating a strong local distribution network.

1. **Maharashtra to Maharashtra:** 2,406 trips
2. **Karnataka to Karnataka:** 2,015 trips
3. **Tamil Nadu to Tamil Nadu:** 1,016 trips
4. **Haryana to Haryana:** 871 trips
5. **Telangana to Telangana:** 655 trips

### Top Logistics Hubs (States)

**Outbound (Source):**
1. Maharashtra (2,682 trips)
2. Karnataka (2,229 trips)
3. Haryana (1,684 trips)
4. Tamil Nadu (1,085 trips)
5. Delhi (793 trips)

**Inbound (Destination):**
1. Maharashtra (2,591 trips)
2. Karnataka (2,276 trips)
3. Haryana (1,667 trips)
4. Tamil Nadu (1,072 trips)
5. Telangana (838 trips)

### Recommendations
1. **Optimize Intra-State Logistics:** Since the highest volume is within states (MH, KA, TN), focus on optimizing local fleet efficiency and micro-fulfillment centers in these regions.
2. **Investigate OSRM Accuracy:** The significant deviation between OSRM and Actual times warrants a deep dive. Consider adjusting the routing algorithm parameters or adding "buffer times" based on historical data to improve delivery estimates.
3. **Hub Capacity Planning:** Maharashtra and Karnataka are the critical hubs for both inbound and outbound traffic. Ensure these states have sufficient warehousing and processing capacity.

## 4. Technical Implementation
- **Script:** `delhivery_solution.py`
- **Process:** 
  - Data cleaning (state/city name standardization)
  - Feature engineering (time conversion to hours)
  - Aggregation (Trip UUID level)
  - Statistical validation (KS Tests)
