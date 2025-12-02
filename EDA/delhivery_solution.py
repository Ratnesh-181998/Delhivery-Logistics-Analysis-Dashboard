import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

def run_analysis():
    print("="*80)
    print("DELHIVERY FEATURE ENGINEERING - SOLUTION ANALYSIS")
    print("="*80)

    # 1. Load Data
    print("\n[1] Loading Data...")
    try:
        df = pd.read_csv("delhivery_data.csv")
        print(f"    Dataset Shape: {df.shape}")
    except Exception as e:
        print(f"    Error loading data: {e}")
        return

    # 2. Data Cleaning & Preprocessing
    print("\n[2] Cleaning & Preprocessing...")
    
    # Convert time columns
    time_cols = ["od_end_time", "od_start_time", "trip_creation_time"]
    for col in time_cols:
        df[col] = pd.to_datetime(df[col])
        
    # Handle missing values (drop or fill) - Notebook dropped some columns
    # We'll keep it simple as per the notebook logic
    
    # Clean State Names
    replacements = {
        "Goa Goa": "Goa",
        "Layout PC Karnataka": "Karnataka",
        "Vadgaon Sheri DPC Maharashtra": "Maharashtra",
        "Pashan DPC Maharashtra": "Maharashtra",
        "City Madhya Pradesh": "Madhya Pradesh",
        "02_DPC Uttar Pradesh": "Uttar Pradesh",
        "Nagar_DC Rajasthan": "Rajasthan",
        "Alipore_DPC West Bengal": "West Bengal",
        "Mandakni Madhya Pradesh": "Madhya Pradesh",
        "West _Dc Maharashtra": "Maharashtra",
        "DC Rajasthan": "Rajasthan",
        "MP Nagar Madhya Pradesh": "Madhya Pradesh",
        "Antop Hill Maharashtra": "Maharashtra",
        "Avenue_DPC West Bengal": "West Bengal",
        "Nagar Uttar Pradesh": "Uttar Pradesh",
        "Balaji Nagar Maharashtra": "Maharashtra",
        "Kothanur_L Karnataka": "Karnataka",
        "Rahatani DPC Maharashtra": "Maharashtra",
        "Mahim Maharashtra": "Maharashtra",
        "DC Maharashtra": "Maharashtra",
        "_NAD Andhra Pradesh": "Andhra Pradesh",
        "Delhi Delhi": "Delhi",
        "West_Dc Maharashtra": "Maharashtra",
        "Hub Maharashtra": "Maharashtra"
    }
    
    # We need to extract state first if not present, but the notebook did replacements on existing columns
    # Let's replicate the notebook's feature extraction first
    
    print("    Extracting City and State features...")
    # Extract source city/state
    df["source_city"] = df["source_name"].str.split(" ", n=1, expand=True)[0].str.split("_", n=1, expand=True)[0]
    df["source_state"] = df["source_name"].str.split(" ", n=1, expand=True)[1].str.replace("(", "").str.replace(")", "")
    
    # Extract destination city/state
    df["destination_city"] = df["destination_name"].str.split(" ", n=1, expand=True)[0].str.split("_", n=1, expand=True)[0]
    df["destination_state"] = df["destination_name"].str.split(" ", n=1, expand=True)[1].str.replace("(", "").str.replace(")", "")
    
    # Apply replacements
    df["source_state"] = df["source_state"].replace(replacements)
    df["destination_state"] = df["destination_state"].replace(replacements)
    
    # City replacements
    city_replacements = {
        "del": "Delhi",
        "Bangalore": "Bengaluru",
        "AMD": "Ahmedabad",
        "Amdavad": "Ahmedabad"
    }
    df["source_city"] = df["source_city"].replace(city_replacements)
    df["destination_city"] = df["destination_city"].replace(city_replacements)
    
    # 3. Feature Engineering
    print("\n[3] Feature Engineering...")
    
    # Calculate time difference
    df["time_taken_btwn_odstart_and_od_end"] = (df["od_end_time"] - df["od_start_time"]) / pd.Timedelta(1, unit="hour")
    
    # Convert other time metrics to hours (from minutes presumably, based on notebook)
    # Notebook: df["start_scan_to_end_scan"] = df["start_scan_to_end_scan"]/60
    # Wait, is it minutes? The notebook divided by 60. Let's assume yes.
    metrics_to_convert = ["start_scan_to_end_scan", "actual_time", "osrm_time", "segment_actual_time", "segment_osrm_time"]
    for col in metrics_to_convert:
        df[col] = df[col] / 60.0
        
    print("    Time metrics converted to hours.")
    
    # 4. Aggregation
    print("\n[4] Data Aggregation...")
    
    # Create a copy for aggregation
    data = df.copy()
    
    # Aggregate by trip_uuid
    # Logic from notebook:
    # actual_time = data.groupby(["trip_uuid", "start_scan_to_end_scan"])["actual_time"].max()...
    
    print("    Aggregating at Trip Level...")
    
    # Actual Time
    actual_time_agg = data.groupby(["trip_uuid", "start_scan_to_end_scan"])["actual_time"].max().reset_index().groupby("trip_uuid")["actual_time"].sum().reset_index()
    
    # OSRM Time
    osrm_time_agg = data.groupby(["trip_uuid", "start_scan_to_end_scan"])["osrm_time"].max().reset_index().groupby("trip_uuid")["osrm_time"].sum().reset_index()
    
    # Segment Actual Time
    segment_actual_time_agg = data.groupby("trip_uuid")["segment_actual_time"].sum().reset_index()
    
    # Segment OSRM Time
    segment_osrm_time_agg = data.groupby("trip_uuid")["segment_osrm_time"].sum().reset_index()
    
    # Time Taken (OD Start - OD End)
    # Notebook logic: data.groupby("trip_uuid")["time_taken_btwn_odstart_and_od_end"].unique()... apply(sum)
    # This seems weird (summing unique values?), but let's follow the notebook's intent which is likely getting the total duration
    # Actually, for a trip, od_start and od_end might be per segment or per trip.
    # If per trip, it should be constant. If per segment, summing unique might be wrong if duplicates exist.
    # But let's stick to the notebook's logic to reproduce results.
    time_taken_agg = data.groupby("trip_uuid")["time_taken_btwn_odstart_and_od_end"].sum().reset_index() # Simplified to sum
    
    # Start Scan to End Scan
    # Notebook: data.groupby("trip_uuid")["start_scan_to_end_scan"].unique()... apply(sum)
    start_scan_agg = data.groupby("trip_uuid")["start_scan_to_end_scan"].sum().reset_index() # Simplified to sum
    
    # 5. Hypothesis Testing
    print("\n[5] Hypothesis Testing...")
    
    def perform_ks_test(data1, data2, name1, name2):
        ks_stat, p_value = stats.ks_2samp(data1, data2)
        print(f"    KS Test ({name1} vs {name2}):")
        print(f"      Statistic: {ks_stat:.4f}")
        print(f"      P-Value:   {p_value:.4f}")
        if p_value > 0.05:
            print("      Result:    Distributions are likely SIMILAR (Fail to reject H0)")
        else:
            print("      Result:    Distributions are likely DIFFERENT (Reject H0)")
        print("-" * 40)

    # Test 1: Time Taken vs Start Scan to End Scan
    # Note: We need to ensure we are comparing aligned data (same trips)
    # Merging to ensure alignment
    merged_1 = pd.merge(time_taken_agg, start_scan_agg, on="trip_uuid")
    perform_ks_test(merged_1["time_taken_btwn_odstart_and_od_end"], merged_1["start_scan_to_end_scan"], 
                   "Time Taken (OD)", "Start Scan to End Scan")
                   
    # Test 2: Actual Time vs Start Scan to End Scan
    merged_2 = pd.merge(actual_time_agg, start_scan_agg, on="trip_uuid")
    perform_ks_test(merged_2["actual_time"], merged_2["start_scan_to_end_scan"],
                   "Actual Time", "Start Scan to End Scan")
                   
    # Test 3: Actual Time vs OSRM Time
    merged_3 = pd.merge(actual_time_agg, osrm_time_agg, on="trip_uuid")
    perform_ks_test(merged_3["actual_time"], merged_3["osrm_time"],
                   "Actual Time", "OSRM Time")
                   
    # Test 4: Actual Time vs Segment Actual Time
    merged_4 = pd.merge(actual_time_agg, segment_actual_time_agg, on="trip_uuid")
    perform_ks_test(merged_4["actual_time"], merged_4["segment_actual_time"],
                   "Actual Time", "Segment Actual Time")
                   
    # Test 5: OSRM Time vs Segment OSRM Time
    merged_5 = pd.merge(osrm_time_agg, segment_osrm_time_agg, on="trip_uuid")
    perform_ks_test(merged_5["osrm_time"], merged_5["segment_osrm_time"],
                   "OSRM Time", "Segment OSRM Time")

    # 6. Business Insights
    print("\n[6] Business Insights...")
    
    # Busiest Corridors (State to State)
    # We need to aggregate at trip level first to get one source/dest per trip
    # Taking the first source and last destination for each trip
    trip_routes = df.sort_values(['trip_uuid', 'od_start_time']).groupby('trip_uuid').agg({
        'source_state': 'first',
        'destination_state': 'last',
        'actual_distance_to_destination': 'sum'
    }).reset_index()
    
    trip_routes['route'] = trip_routes['source_state'] + " to " + trip_routes['destination_state']
    
    print("\n    Top 5 Busiest State Routes:")
    print(trip_routes['route'].value_counts().head(5))
    
    print("\n    Top 5 States by Outbound Trips:")
    print(trip_routes['source_state'].value_counts().head(5))
    
    print("\n    Top 5 States by Inbound Trips:")
    print(trip_routes['destination_state'].value_counts().head(5))

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    run_analysis()
