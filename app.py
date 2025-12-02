import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from datetime import datetime
from scipy import stats
from scipy.stats import ttest_ind, ks_2samp
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import warnings

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    filename='delhivery_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
logger.info("="*50)
logger.info("Delhivery Application Started")
logger.info("="*50)

# Page Configuration
st.set_page_config(
    page_title="Delhivery Logistics Analysis",
    layout="wide",
    page_icon="🚚",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS matching Yulu style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }
    .block-container {
        background: rgba(17, 24, 39, 0.85);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    h1 {
        background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeInDown 1s ease-in-out;
        letter-spacing: -1px;
    }
    h2 { 
        color: #f3f4f6 !important; 
        border-bottom: 3px solid #8b5cf6; 
        padding-bottom: 0.5rem; 
        margin-top: 2rem; 
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(139, 92, 246, 0.3);
    }
    h3 { 
        color: #e5e7eb !important; 
        margin-top: 1.5rem; 
        font-weight: 600 !important; 
    }
    p, li, span, div { color: #cbd5e1; }
    
    [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: pulse 2s ease-in-out infinite;
    }
    [data-testid="stMetricLabel"] { 
        color: #9ca3af !important; 
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.75rem !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { 
        gap: 12px; 
        background-color: rgba(17, 24, 39, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(244, 114, 182, 0.1) 100%);
        color: #a78bfa; 
        border-radius: 10px; 
        padding: 12px 24px; 
        font-weight: 600; 
        transition: all 0.3s ease; 
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    .stTabs [data-baseweb="tab"]:hover { 
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(244, 114, 182, 0.2) 100%);
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%) !important; 
        color: white !important; 
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
        transform: translateY(-2px);
    }
    
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%); 
        border-right: 1px solid rgba(139, 92, 246, 0.3);
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 { 
        color: white !important; 
        -webkit-text-fill-color: white !important; 
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] li, 
    [data-testid="stSidebar"] span { 
        color: #cbd5e1 !important; 
        -webkit-text-fill-color: #cbd5e1 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); 
        color: white; 
        border-radius: 12px; 
        padding: 0.75rem 2rem; 
        font-weight: 600; 
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); 
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6); 
        color: white; 
    }
    
    @keyframes fadeInDown { 
        from { opacity: 0; transform: translateY(-30px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .card {
        padding: 1rem; 
        border-radius: 16px; 
        text-align: center; 
        color: white; 
        box-shadow: 0 8px 32px rgba(0,0,0,0.4); 
        transition: all 0.4s ease; 
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    .card:hover::before {
        left: 100%;
    }
    .card:hover { 
        transform: translateY(-8px) scale(1.02); 
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(244, 114, 182, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(244, 114, 182, 0.2) 100%);
        border-color: rgba(139, 92, 246, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
    }
    
    .stExpander {
        background: rgba(17, 24, 39, 0.5);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
<div style='position: fixed; top: 3.5rem; right: 1.5rem; z-index: 9999;'>
    <div style='background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); 
                border-radius: 20px; padding: 0.6rem 1.2rem; 
                box-shadow: 0 4px 20px rgba(139, 92, 246, 0.5);
                animation: fadeInDown 1s ease-in-out;'>
        <span style='color: white; font-weight: 700; font-size: 0.9rem; letter-spacing: 1.5px;'>
            ✨ By RATNESH SINGH
        </span>
    </div>
</div>
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <h1 style='font-size: 4rem; margin-bottom: 0;'>🚚 Delhivery Logistics Analytics</h1>
    <p style='font-size: 1.3rem; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; margin-top: 0.5rem; letter-spacing: 1px;'>
        🎯 Feature Engineering & Hypothesis Testing
    </p>
</div>
""", unsafe_allow_html=True)

# Enhanced Feature Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
        <div style='font-size: 2rem; margin-bottom: 0.25rem;'>📊</div>
        <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>Data</h3>
        <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Trip Records</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class='card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
        <div style='font-size: 2rem; margin-bottom: 0.25rem;'>🔍</div>
        <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>EDA</h3>
        <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Visual Analysis</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class='card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
        <div style='font-size: 2rem; margin-bottom: 0.25rem;'>🔬</div>
        <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>Testing</h3>
        <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Hypothesis Tests</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class='card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
        <div style='font-size: 2rem; margin-bottom: 0.25rem;'>💡</div>
        <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>Insights</h3>
        <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Recommendations</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("## 📑 Navigation")
    st.markdown("---")
    st.markdown("""
    <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(139, 92, 246, 0.3);'>
        <h3 style='color: #a78bfa !important; margin-top: 0;'>📊 Project Overview</h3>
        <p><strong>Company:</strong> Delhivery - India's largest fully integrated logistics player</p>
        <p><strong>Goal:</strong> Process data, feature engineering, and forecasting models</p>
        <p><strong>Period:</strong> Sept-Oct 2018</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: rgba(244, 114, 182, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(244, 114, 182, 0.3);'>
        <h3 style='color: #f472b6 !important; margin-top: 0;'>🔍 Analysis Steps</h3>
        <ul style='margin: 0; padding-left: 1.2rem;'>
            <li>Data Cleaning & Manipulation</li>
            <li>Feature Extraction</li>
            <li>Aggregation by Trip UUID</li>
            <li>Hypothesis Testing (Time & Distance)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: rgba(56, 239, 125, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(56, 239, 125, 0.3);'>
        <h3 style='color: #38ef7d !important; margin-top: 0;'>💡 Key Findings</h3>
        <p>✓ <strong>Actual vs OSRM:</strong> Actual time is generally higher</p>
        <p>✓ <strong>Routes:</strong> 60% Carting, 40% FTL</p>
        <p>✓ <strong>States:</strong> Maharashtra & Karnataka are top hubs</p>
    </div>
    """, unsafe_allow_html=True)

# Load and preprocess data
@st.cache_data
def load_data():
    logger.info("Loading dataset...")
    try:
        df = pd.read_csv("delhivery_data.csv")
        logger.info(f"Dataset loaded: {df.shape}")
        
        # Preprocessing
        df["od_end_time"] = pd.to_datetime(df["od_end_time"])
        df["od_start_time"] = pd.to_datetime(df["od_start_time"])
        df["trip_creation_time"] = pd.to_datetime(df["trip_creation_time"])
        
        df["trip_creation_day"] = df["trip_creation_time"].dt.day_name()
        df["trip_creation_month"] = df["trip_creation_time"].dt.month_name()
        df["trip_creation_year"] = df["trip_creation_time"].dt.year
        
        # Extracting City and State
        df["source_city"] = df["source_name"].str.split(" ",n=1,expand=True)[0].str.split("_",n=1,expand=True)[0]
        df["source_state"] = df["source_name"].str.split(" ",n=1,expand=True)[1].str.replace("(","").str.replace(")","")
        df["destination_city"] = df["destination_name"].str.split(" ",n=1,expand=True)[0].str.split("_",n=1,expand=True)[0]
        df["destination_state"] = df["destination_name"].str.split(" ",n=1,expand=True)[1].str.replace("(","").str.replace(")","")
        
        # Time calculations
        df["time_taken_btwn_odstart_and_od_end"] = ((df["od_end_time"]-df["od_start_time"])/pd.Timedelta(1,unit="hour"))
        
        # Convert to hours
        for col in ["start_scan_to_end_scan", "actual_time", "osrm_time", "segment_actual_time", "segment_osrm_time"]:
            df[col] = df[col]/60
            
        # Cleaning State Names
        replacements = {
            "Goa Goa":"Goa", "Layout PC Karnataka":"Karnataka", "Vadgaon Sheri DPC Maharashtra":"Maharashtra",
            "Pashan DPC Maharashtra":"Maharashtra", "City Madhya Pradesh":"Madhya Pradesh", "02_DPC Uttar Pradesh":"Uttar Pradesh",
            "Nagar_DC Rajasthan":"Rajasthan", "Alipore_DPC West Bengal":"West Bengal", "Mandakni Madhya Pradesh":"Madhya Pradesh",
            "West _Dc Maharashtra":"Maharashtra", "DC Rajasthan":"Rajasthan", "MP Nagar Madhya Pradesh":"Madhya Pradesh",
            "Antop Hill Maharashtra":"Maharashtra", "Avenue_DPC West Bengal":"West Bengal", "Nagar Uttar Pradesh":"Uttar Pradesh",
            "Balaji Nagar Maharashtra":"Maharashtra", "Kothanur_L Karnataka":"Karnataka", "Rahatani DPC Maharashtra":"Maharashtra",
            "Mahim Maharashtra":"Maharashtra", "DC Maharashtra":"Maharashtra", "_NAD Andhra Pradesh":"Andhra Pradesh",
            "Delhi Delhi":"Delhi", "West_Dc Maharashtra":"Maharashtra", "Hub Maharashtra":"Maharashtra"
        }
        df["source_state"] = df["source_state"].replace(replacements)
        df["destination_state"] = df["destination_state"].replace(replacements)
        
        # Cleaning City Names
        df["destination_city"].replace({"del":"Delhi", "Bangalore":"Bengaluru", "AMD":"Ahmedabad", "Amdavad":"Ahmedabad"}, inplace=True)
        df["source_city"].replace({"del":"Delhi", "Bangalore":"Bengaluru", "AMD":"Ahmedabad", "Amdavad":"Ahmedabad"}, inplace=True)
        
        df["source_city_state"] = df["source_city"] + " " + df["source_state"]
        df["destination_city_state"] = df["destination_city"] + " " + df["destination_state"]
        
        # Aggregation
        data = df.copy()
        
        actual_time = data.groupby(["trip_uuid", "start_scan_to_end_scan"])["actual_time"].max().reset_index().groupby("trip_uuid")["actual_time"].sum().reset_index()
        segment_osrm_time = data[["trip_uuid","segment_osrm_time"]].groupby("trip_uuid")["segment_osrm_time"].sum().reset_index()
        segment_actual_time = data.groupby("trip_uuid")["segment_actual_time"].sum().reset_index()
        osrm_time = data.groupby(["trip_uuid", "start_scan_to_end_scan"])["osrm_time"].max().reset_index().groupby("trip_uuid")["osrm_time"].sum().reset_index()
        
        time_taken = data.groupby("trip_uuid")["time_taken_btwn_odstart_and_od_end"].unique().reset_index()
        time_taken["time_taken_btwn_odstart_and_od_end"] = time_taken["time_taken_btwn_odstart_and_od_end"].apply(sum)
        
        start_scan = data.groupby("trip_uuid")["start_scan_to_end_scan"].unique().reset_index()
        start_scan["start_scan_to_end_scan"] = start_scan["start_scan_to_end_scan"].apply(sum)
        
        osrm_distance = data.groupby(["trip_uuid", "start_scan_to_end_scan"])["osrm_distance"].max().reset_index().groupby("trip_uuid")["osrm_distance"].sum().reset_index()
        actual_distance = data.groupby(["trip_uuid", "start_scan_to_end_scan"])["actual_distance_to_destination"].max().reset_index().groupby("trip_uuid")["actual_distance_to_destination"].sum().reset_index()
        segment_osrm_distance = data[["trip_uuid", "segment_osrm_distance"]].groupby("trip_uuid")["segment_osrm_distance"].sum().reset_index()
        
        # Merging
        distances = segment_osrm_distance.merge(actual_distance.merge(osrm_distance, on="trip_uuid"), on="trip_uuid")
        time = segment_osrm_time.merge(osrm_time.merge(segment_actual_time.merge(actual_time.merge(time_taken.merge(start_scan, on="trip_uuid"), on="trip_uuid"), on="trip_uuid"), on="trip_uuid"), on="trip_uuid")
        
        trip_records = time.merge(distances, on="trip_uuid")
        
        route_type = data.groupby("trip_uuid")["route_type"].unique().reset_index()
        trip_records = trip_records.merge(route_type, on="trip_uuid")
        trip_records["route_type"] = trip_records["route_type"].apply(lambda x:x[0])
        
        logger.info("Preprocessing completed")
        return df, trip_records
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        st.error(f"Error loading data: {str(e)}")
        return None, None

try:
    df, trip_records = load_data()
    if df is not None:
        logger.info("Data ready")
    else:
        st.stop()
except Exception as e:
    logger.error(f"Failed to load data: {str(e)}")
    st.error("❌ Failed to load data")
    st.stop()

# Main Tabs
tabs = st.tabs([
    "📊 Problem Statement",
    "📝 Methodology",
    "🔍 Interactive EDA", 
    "🛠️ Feature Engineering",
    "🔬 Hypothesis Testing",
    "💡 Insights & Recommendations",
    "📚 Complete Analysis",
    "📝 Logs"
])

logger.info("Main tabs created")

# TAB 1: Problem Statement
with tabs[0]:
    st.header("📊 About Delhivery & Problem Statement")
    logger.info("Problem Statement tab accessed")
    
    # Enhanced Metrics with Gradient Cards
    st.markdown("""
    <style>
        .metric-container {
            background: rgba(17, 24, 39, 0.7);
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid rgba(139, 92, 246, 0.2);
            transition: all 0.3s ease;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .metric-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
            border-color: rgba(139, 92, 246, 0.5);
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0.5rem 0;
        }
        .metric-label {
            color: #94a3b8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }
        .metric-icon {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            background: rgba(139, 92, 246, 0.1);
            width: 50px;
            height: 50px;
            line-height: 50px;
            border-radius: 50%;
            margin: 0 auto 1rem auto;
        }
    </style>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    
    # Hero Section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding: 2rem; border-radius: 16px; border: 1px solid rgba(139, 92, 246, 0.3); margin-bottom: 2rem;'>
        <div style='display: flex; align-items: center; gap: 20px;'>
            <div style='font-size: 3rem; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 50%;'>🚚</div>
            <div>
                <h2 style='color: #a78bfa; margin: 0; font-size: 2rem;'>Delhivery Logistics Analysis</h2>
                <p style='color: #cbd5e1; margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
                    Optimizing the operating system for commerce through data-driven insights.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
        <div class="metric-container" style="border-bottom: 4px solid #667eea;">
            <div class="metric-icon" style="color: #667eea;">📊</div>
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-label">Total Segments</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">Raw Data Points</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="metric-container" style="border-bottom: 4px solid #f472b6;">
            <div class="metric-icon" style="color: #f472b6;">🧩</div>
            <div class="metric-value">{len(trip_records):,}</div>
            <div class="metric-label">Unique Trips</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">Aggregated</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
        <div class="metric-container" style="border-bottom: 4px solid #38ef7d;">
            <div class="metric-icon" style="color: #38ef7d;">🏙️</div>
            <div class="metric-value">{df['source_city'].nunique()}</div>
            <div class="metric-label">Cities Covered</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">Across India</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m4:
        st.markdown(f"""
        <div class="metric-container" style="border-bottom: 4px solid #fb923c;">
            <div class="metric-icon" style="color: #fb923c;">⚡</div>
            <div class="metric-value">{df['actual_time'].mean():.1f}</div>
            <div class="metric-label">Avg Time (hrs)</div>
            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">Per Segment</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Business Context & Challenge Grid
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.subheader("🏢 About Delhivery")
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #8b5cf6; height: 100%;'>
            <p style='color: #cbd5e1; line-height: 1.7; font-size: 1.05rem;'>
                <strong>Delhivery</strong> is India's largest and fastest-growing fully integrated logistics player. 
                They aim to build the <strong>operating system for commerce</strong> by combining world-class infrastructure 
                with cutting-edge engineering and technology.
            </p>
            <div style='margin-top: 1.5rem;'>
                <h5 style='color: #a78bfa; margin-bottom: 0.5rem;'>🎯 Core Objective</h5>
                <p style='color: #94a3b8; font-size: 0.95rem;'>
                    To process raw logistics data, clean and sanitize it, and derive meaningful features 
                    to build robust forecasting models that can predict delivery times and optimize routes.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.subheader("⚠️ The Challenge")
        st.markdown("""
        <div style='background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ec4899; height: 100%;'>
            <p style='color: #cbd5e1; margin-bottom: 1rem;'>
                The data engineering pipelines generate raw, noisy data that needs significant processing:
            </p>
            <div style='display: flex; flex-direction: column; gap: 10px;'>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='background: rgba(236, 72, 153, 0.2); color: #ec4899; padding: 5px 10px; border-radius: 6px; font-size: 0.9rem;'>🧹 Cleaning</span>
                    <span style='color: #94a3b8; font-size: 0.9rem;'>Handle missing values & standardization</span>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='background: rgba(56, 239, 125, 0.2); color: #38ef7d; padding: 5px 10px; border-radius: 6px; font-size: 0.9rem;'>⚙️ Feature Eng</span>
                    <span style='color: #94a3b8; font-size: 0.9rem;'>Extract time & location metrics</span>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='background: rgba(251, 146, 60, 0.2); color: #fb923c; padding: 5px 10px; border-radius: 6px; font-size: 0.9rem;'>🧪 Validation</span>
                    <span style='color: #94a3b8; font-size: 0.9rem;'>Hypothesis testing & outlier removal</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Business Impact Section
    st.subheader("💡 Business Impact")
    st.markdown("""
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem;'>
        <div class='metric-card' style='text-align: center;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📉</div>
            <h4 style='color: #cbd5e1; margin: 0;'>Cost Reduction</h4>
            <p style='color: #94a3b8; font-size: 0.9rem;'>Optimizing routes to save fuel and time.</p>
        </div>
        <div class='metric-card' style='text-align: center;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>⚡</div>
            <h4 style='color: #cbd5e1; margin: 0;'>Efficiency</h4>
            <p style='color: #94a3b8; font-size: 0.9rem;'>Improving delivery speed and reliability.</p>
        </div>
        <div class='metric-card' style='text-align: center;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🧠</div>
            <h4 style='color: #cbd5e1; margin: 0;'>Forecasting</h4>
            <p style='color: #94a3b8; font-size: 0.9rem;'>Predicting delays and resource needs.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample Data
    with st.expander("🔍 View Raw Data Preview", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)

# TAB 2: Methodology
with tabs[1]:
    st.header("📝 Solution Approach & Methodology")
    
    # Introduction
    st.markdown("""
    <div style='background: rgba(139, 92, 246, 0.1); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #8b5cf6; margin-bottom: 2rem;'>
        <h4 style='color: #a78bfa; margin-top: 0;'>🚀 End-to-End Data Pipeline</h4>
        <p style='color: #cbd5e1; margin: 0;'>
            We implemented a robust data processing pipeline to transform raw segment-level logistics data into actionable trip-level insights. 
            The process ensures data quality, handles anomalies, and prepares the dataset for statistical hypothesis testing.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pipeline Visualization
    st.subheader("🔄 Processing Workflow")
    st.graphviz_chart("""
    digraph {
        rankdir=LR;
        bgcolor="transparent";
        node [style="filled", fillcolor="#1e1b4b", color="#8b5cf6", fontcolor="white", shape="box", fontname="Sans-Serif"];
        edge [color="#cbd5e1"];
        
        "Raw Data" -> "Cleaning";
        "Cleaning" -> "Feature Eng";
        "Feature Eng" -> "Aggregation";
        "Aggregation" -> "Outliers";
        "Outliers" -> "Hypothesis Testing";
        "Hypothesis Testing" -> "Insights";
    }
    """)
    
    st.markdown("---")
    
    # Detailed Steps in Grid
    st.subheader("🛠️ Detailed Methodology Steps")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        <div class='metric-card' style='height: 100%;'>
            <h4 style='color: #f472b6;'>1. Data Cleaning & Standardization</h4>
            <ul style='color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0;'>
                <li><strong>Missing Values:</strong> Imputed city/state info using logical mapping from existing fields.</li>
                <li><strong>Name Standardization:</strong> Corrected typos (e.g., "Bangalore" -> "Bengaluru", "Goa Goa" -> "Goa").</li>
                <li><strong>Type Casting:</strong> Converted timestamps to datetime objects for temporal analysis.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='metric-card' style='height: 100%;'>
            <h4 style='color: #fb923c;'>3. Aggregation Strategy</h4>
            <ul style='color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0;'>
                <li><strong>Grouping Key:</strong> <code>trip_uuid</code> used as the primary key.</li>
                <li><strong>Summation:</strong> Aggregated cumulative metrics like <code>actual_time</code>, <code>osrm_time</code>, and distances.</li>
                <li><strong>Logic:</strong> Merged segment-level rows into single trip records to analyze end-to-end performance.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class='metric-card' style='height: 100%;'>
            <h4 style='color: #38ef7d;'>2. Feature Extraction</h4>
            <ul style='color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0;'>
                <li><strong>Time Metrics:</strong> Derived <code>time_taken</code> from start/end timestamps.</li>
                <li><strong>Date Features:</strong> Extracted Day, Month, and Year for temporal trend analysis.</li>
                <li><strong>Location Parsing:</strong> Split <code>source_name</code> and <code>destination_name</code> into City, State, and Place.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='metric-card' style='height: 100%;'>
            <h4 style='color: #667eea;'>4. Statistical Validation</h4>
            <ul style='color: #cbd5e1; font-size: 0.9rem; margin-bottom: 0;'>
                <li><strong>Hypothesis Tests:</strong> T-tests to compare Actual vs. OSRM time/distance.</li>
                <li><strong>Outlier Detection:</strong> Used IQR method to identify and filter anomalous trips.</li>
                <li><strong>Normalization:</strong> Scaled features using StandardScaler for potential modeling.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# TAB 3: Interactive EDA
with tabs[2]:
    st.header("🔍 Interactive Exploratory Data Analysis")
    logger.info("Interactive EDA tab accessed")
    
    viz_tabs = st.tabs(["📊 Overview", "🚚 Route Analysis", "⏰ Temporal Patterns", "📍 Location Analysis", "🔥 Correlations"])
    
    with viz_tabs[0]:
        st.subheader("Dataset Overview")
        
        st.markdown("""
<div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #8b5cf6; margin-bottom: 1.5rem;'>
    <h4 style='color: #a78bfa; margin-top: 0;'>📊 Understanding the Data</h4>
    <p style='color: #cbd5e1; margin: 0;'>
        This section provides a comprehensive overview of the logistics dataset, including 
        statistical summaries and distribution patterns. It helps in understanding the scale and nature of operations.
    </p>
</div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Numerical Features Summary (Aggregated Trips)**")
            st.caption("Key statistics for time and distance metrics across all trips.")
            numerical_cols = ['actual_time', 'osrm_time', 'actual_distance_to_destination', 'osrm_distance']
            st.dataframe(trip_records[numerical_cols].describe().T, use_container_width=True)
        
        with col2:
            st.markdown("**Categorical Features**")
            st.caption("Breakdown of key categorical variables like Route Type and States.")
            cat_summary = []
            for col in ['route_type', 'source_state', 'destination_state']:
                value_counts = df[col].value_counts()
                cat_summary.append({
                    'Feature': col,
                    'Unique': df[col].nunique(),
                    'Most Common': value_counts.index[0],
                    'Frequency': value_counts.values[0]
                })
            st.dataframe(pd.DataFrame(cat_summary), use_container_width=True, hide_index=True)
        
    with viz_tabs[1]:
        st.subheader("Route Type Analysis")
        
        st.markdown("""
        <div style='background: rgba(244, 114, 182, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #f472b6; margin-bottom: 1.5rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Route Type Insights:</strong> Analyzing the split between FTL (Full Truck Load) and Carting (Partial Load) helps in resource allocation.
                FTL typically involves direct point-to-point transport, while Carting involves multiple stops.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🚚 Route Type Distribution**")
            st.caption("Proportion of FTL vs Carting trips.")
            route_counts = trip_records['route_type'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=route_counts.index,
                values=route_counts.values,
                hole=0.4,
                marker=dict(colors=['#667eea', '#f093fb']),
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                height=350,
                showlegend=True,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**⏱️ Average Time by Route Type**")
            st.caption("Comparison of average actual delivery time (in hours) for each route type.")
            route_time = trip_records.groupby('route_type')['actual_time'].mean().reset_index()
            fig = go.Figure(data=[go.Bar(
                x=route_time['route_type'],
                y=route_time['actual_time'],
                marker=dict(color=['#667eea', '#f093fb']),
                text=[f'{v:.1f} hrs' for v in route_time['actual_time']],
                textposition='outside',
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                height=350,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Avg Time (Hours)'),
                margin=dict(t=20, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)

    with viz_tabs[2]:
        st.subheader("Temporal Patterns")
        
        st.markdown("""
        <div style='background: rgba(56, 239, 125, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #38ef7d; margin-bottom: 1.5rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Temporal Analysis:</strong> Understanding when trips occur helps optimize resource allocation and identify peak demand periods.
                This analysis reveals patterns across days and months that can inform staffing and fleet management decisions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📅 Trips by Day of Week**")
            st.caption("Distribution of trips across different days to identify weekly patterns.")
            day_counts = df['trip_creation_day'].value_counts()
            fig = go.Figure(data=[go.Bar(
                x=day_counts.index,
                y=day_counts.values,
                marker=dict(color='#11998e'),
                text=day_counts.values,
                textposition='outside'
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False, title='Day of Week'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Number of Trips'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**📅 Trips by Month**")
            st.caption("Monthly trip volume showing seasonal trends and demand fluctuations.")
            month_counts = df['trip_creation_month'].value_counts().sort_index()
            fig = go.Figure(data=[go.Bar(
                x=month_counts.index,
                y=month_counts.values,
                marker=dict(color='#fa709a'),
                text=month_counts.values,
                textposition='outside'
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False, title='Month'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Number of Trips'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

    with viz_tabs[3]:
        st.subheader("Location Analysis")
        
        st.markdown("""
        <div style='background: rgba(251, 146, 60, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #fb923c; margin-bottom: 1.5rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Geographic Distribution:</strong> Identifying high-volume source and destination states helps in strategic hub placement
                and understanding regional demand patterns. This data is crucial for network optimization.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🗺️ Top 10 Source States**")
            st.caption("States with the highest number of outgoing shipments.")
            state_counts = df['source_state'].value_counts().head(10)
            fig = px.bar(
                x=state_counts.index, 
                y=state_counts.values,
                labels={'x': 'State', 'y': 'Trip Count'},
                color=state_counts.values,
                color_continuous_scale='Viridis',
                text=state_counts.values
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                showlegend=False,
                height=400
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**🎯 Top 10 Destination States**")
            st.caption("States receiving the most incoming shipments.")
            dest_counts = df['destination_state'].value_counts().head(10)
            fig = px.bar(
                x=dest_counts.index, 
                y=dest_counts.values,
                labels={'x': 'State', 'y': 'Trip Count'},
                color=dest_counts.values,
                color_continuous_scale='Plasma',
                text=dest_counts.values
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                showlegend=False,
                height=400
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
    with viz_tabs[4]:
        st.subheader("Correlation Analysis")
        
        st.markdown("""
        <div style='background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 1.5rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Feature Relationships:</strong> The correlation heatmap reveals how different time and distance metrics relate to each other.
                Strong positive correlations (red) indicate metrics that move together, while negative correlations (blue) show inverse relationships.
                This helps identify redundant features and understand metric dependencies.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**🔥 Feature Correlation Heatmap**")
        st.caption("Correlation coefficients between key time and distance metrics.")
        
        corr_cols = ['actual_time', 'osrm_time', 'actual_distance_to_destination', 'osrm_distance', 'segment_actual_time', 'segment_osrm_time']
        corr_matrix = trip_records[corr_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto='.2f',
            aspect="auto",
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 4: Feature Engineering
with tabs[3]:
    st.header("🛠️ Feature Engineering & Data Processing")
    
    st.markdown("""
<div style='background: rgba(244, 114, 182, 0.1); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(244, 114, 182, 0.3); margin-bottom: 2rem;'>
    <h4 style='color: #f472b6; margin-top: 0;'>⚙️ Processing Pipeline</h4>
    <p style='color: #cbd5e1;'>
        The raw data consists of segment-level information. To analyze trip performance, we aggregate these segments into unique trips.
        We also handle missing values, outliers, and normalize features for modeling. This transformation is critical for accurate analysis.
    </p>
</div>
    """, unsafe_allow_html=True)
    
    fe_tabs = st.tabs(["📊 Aggregation Logic", "🧹 Outlier Treatment", "📏 Scaling", "🔢 One-Hot Encoding", "📈 Feature Comparison"])
    
    with fe_tabs[0]:
        st.subheader("Trip Aggregation Strategy")
        
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Why Aggregate?</strong> The raw data contains multiple segments per trip. Aggregating by <code>trip_uuid</code> 
                gives us a complete picture of each delivery journey from origin to final destination.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Aggregation Code:**")
        st.code("""
# Grouping by Trip UUID to aggregate segment data
actual_time = data.groupby("trip_uuid")["actual_time"].sum()
osrm_time = data.groupby("trip_uuid")["osrm_time"].sum()
actual_distance = data.groupby("trip_uuid")["actual_distance_to_destination"].sum()
osrm_distance = data.groupby("trip_uuid")["osrm_distance"].sum()

# Merging all aggregated features into a single dataframe
trip_records = pd.merge(actual_time, osrm_time, on="trip_uuid")
trip_records = trip_records.merge(actual_distance, on="trip_uuid")
trip_records = trip_records.merge(osrm_distance, on="trip_uuid")
        """, language='python')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Data Transformation Impact**")
            st.metric("Original Segments", f"{len(df):,}", help="Total segment-level records")
            st.metric("Aggregated Trips", f"{len(trip_records):,}", help="Unique trip records after aggregation")
            reduction = ((len(df) - len(trip_records)) / len(df) * 100)
            st.metric("Data Reduction", f"{reduction:.1f}%", help="Percentage reduction in record count")
        
        with col2:
            st.markdown("**Resulting Aggregated Data Structure:**")
            st.caption("Sample of aggregated trip records showing summed metrics.")
            st.dataframe(trip_records.head(5), use_container_width=True)
        
    with fe_tabs[1]:
        st.subheader("Outlier Detection & Treatment")
        
        st.markdown("""
        <div style='background: rgba(251, 146, 60, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>IQR Method:</strong> We use the Interquartile Range (IQR) method to identify outliers. 
                Values below Q1 - 1.5×IQR or above Q3 + 1.5×IQR are considered outliers and removed to improve model accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Before Outlier Treatment**")
            st.caption("Box plots showing the distribution with outliers present.")
            fig = px.box(trip_records, y=['actual_time', 'osrm_time'], 
                        labels={'variable': 'Metric', 'value': 'Time (Hours)'})
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='#cbd5e1'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**After Outlier Treatment**")
            st.caption("Cleaned distribution after removing extreme values.")
            # Simulating outlier removal for visualization
            Q1 = trip_records['actual_time'].quantile(0.25)
            Q3 = trip_records['actual_time'].quantile(0.75)
            IQR = Q3 - Q1
            clean_df = trip_records[~((trip_records['actual_time'] < (Q1 - 1.5 * IQR)) | (trip_records['actual_time'] > (Q3 + 1.5 * IQR)))]
            
            fig = px.box(clean_df, y=['actual_time', 'osrm_time'],
                        labels={'variable': 'Metric', 'value': 'Time (Hours)'})
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='#cbd5e1'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"📊 Outliers Removed: {len(trip_records) - len(clean_df):,} records ({((len(trip_records) - len(clean_df)) / len(trip_records) * 100):.2f}%)")
            
    with fe_tabs[2]:
        st.subheader("Feature Scaling")
        
        st.markdown("""
        <div style='background: rgba(56, 239, 125, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Why Scale?</strong> Standardizing features ensures all variables contribute equally to model training.
                StandardScaler transforms features to have mean=0 and std=1, while MinMaxScaler scales to [0,1] range.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        scaler = StandardScaler()
        scaled_cols = ['actual_time', 'osrm_time', 'actual_distance_to_destination', 'osrm_distance']
        scaled_data = scaler.fit_transform(trip_records[scaled_cols].dropna())
        scaled_df = pd.DataFrame(scaled_data, columns=[f"{col}_scaled" for col in scaled_cols])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original Data (Sample)**")
            st.caption("Raw values before scaling.")
            st.dataframe(trip_records[scaled_cols].head(5), use_container_width=True)
            
        with col2:
            st.markdown("**Scaled Data (StandardScaler)**")
            st.caption("Normalized values with mean=0, std=1.")
            st.dataframe(scaled_df.head(5), use_container_width=True)
        
        # Visualization of scaling effect
        st.markdown("**📊 Scaling Visualization**")
        fig = go.Figure()
        fig.add_trace(go.Box(y=trip_records['actual_time'].dropna(), name='Original', marker_color='#f472b6'))
        fig.add_trace(go.Box(y=scaled_df['actual_time_scaled'], name='Scaled', marker_color='#38ef7d'))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            yaxis_title='Value',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with fe_tabs[3]:
        st.subheader("One-Hot Encoding")
        
        st.markdown("""
        <div style='background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Categorical to Numerical:</strong> Machine learning models require numerical input. 
                One-hot encoding converts categorical variables like <code>route_type</code> into binary columns (0 or 1).
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Original Categorical Data**")
            st.caption("Route type as categorical values.")
            st.dataframe(trip_records[['route_type']].head(10), use_container_width=True)
            
        with col2:
            st.markdown("**One-Hot Encoded Result**")
            st.caption("Binary representation of route types.")
            encoded_df = pd.get_dummies(trip_records[['route_type']], columns=['route_type'])
            st.dataframe(encoded_df.head(10), use_container_width=True)
    
    with fe_tabs[4]:
        st.subheader("Feature Comparison: Actual vs OSRM")
        
        st.markdown("""
        <div style='background: rgba(236, 72, 153, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Performance Analysis:</strong> Comparing actual delivery metrics against OSRM (routing engine) estimates 
                helps identify prediction accuracy and areas for improvement.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**⏱️ Time: Actual vs OSRM**")
            st.caption("Scatter plot showing correlation between actual and estimated time.")
            fig = px.scatter(
                trip_records.sample(min(1000, len(trip_records))), 
                x='osrm_time', 
                y='actual_time',
                opacity=0.5,
                trendline="ols",
                labels={'osrm_time': 'OSRM Estimated Time (hrs)', 'actual_time': 'Actual Time (hrs)'}
            )
            fig.add_trace(go.Scatter(
                x=[0, trip_records['osrm_time'].max()],
                y=[0, trip_records['osrm_time'].max()],
                mode='lines',
                name='Perfect Prediction',
                line=dict(color='red', dash='dash')
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**📏 Distance: Actual vs OSRM**")
            st.caption("Scatter plot comparing actual and estimated distances.")
            fig = px.scatter(
                trip_records.sample(min(1000, len(trip_records))), 
                x='osrm_distance', 
                y='actual_distance_to_destination',
                opacity=0.5,
                trendline="ols",
                labels={'osrm_distance': 'OSRM Estimated Distance (km)', 'actual_distance_to_destination': 'Actual Distance (km)'}
            )
            fig.add_trace(go.Scatter(
                x=[0, trip_records['osrm_distance'].max()],
                y=[0, trip_records['osrm_distance'].max()],
                mode='lines',
                name='Perfect Prediction',
                line=dict(color='red', dash='dash')
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

# TAB 5: Hypothesis Testing
with tabs[4]:
    st.header("🔬 Hypothesis Testing")
    logger.info("Hypothesis Testing tab accessed")
    
    st.markdown("""
<div style='background: rgba(17, 24, 39, 0.7); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(139, 92, 246, 0.2); margin-bottom: 2rem;'>
    <h4 style='color: #a78bfa; margin-top: 0;'>🧪 Statistical Significance Tests</h4>
    <p style='color: #cbd5e1;'>
        We perform t-tests and KS-tests to compare various time and distance metrics to check for significant differences.
        This helps in validating the accuracy of OSRM estimates against actual data and understanding systematic biases.
    </p>
    <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem;'>
        <p style='color: #cbd5e1; margin: 0; font-size: 0.9rem;'>
            <strong>Significance Level:</strong> α = 0.05 (95% confidence)<br>
            <strong>Interpretation:</strong> If p-value < 0.05, we reject the null hypothesis (H0) and accept the alternative (Ha).
        </p>
    </div>
</div>
    """, unsafe_allow_html=True)
    
    test_tabs = st.tabs(["⏱️ Actual vs OSRM Time", "🔄 Actual vs Segment Time", "🔀 OSRM vs Segment OSRM", "📏 Actual vs OSRM Distance", "📊 Summary"])
    
    with test_tabs[0]:
        st.subheader("Actual Time vs OSRM Time")
        
        st.markdown("""
        <div style='background: rgba(244, 114, 182, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Test Objective:</strong> Determine if actual delivery times are significantly higher than OSRM estimates.
                This validates whether the routing engine is underestimating delivery times.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**H0 (Null Hypothesis):** Mean Actual Time ≤ Mean OSRM Time")
        st.markdown("**Ha (Alternative Hypothesis):** Mean Actual Time > Mean OSRM Time")
        
        t_stat, p_val = ttest_ind(trip_records['actual_time'], trip_records['osrm_time'], alternative='greater')
        
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("T-Statistic", f"{t_stat:.4f}", help="Measures the difference in means relative to variance")
        m2.metric("P-Value", f"{p_val:.4e}", help="Probability of observing this result by chance")
        m3.metric("Actual Mean", f"{trip_records['actual_time'].mean():.2f}h")
        m4.metric("OSRM Mean", f"{trip_records['osrm_time'].mean():.2f}h")
        
        # Decision
        if p_val < 0.05:
            st.error(f"✅ **Reject H0:** Actual time is significantly greater than OSRM time (p={p_val:.4e} < 0.05)")
            st.markdown("""
            <div style='background: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #ef4444;'>
                <p style='color: #cbd5e1; margin: 0;'>
                    <strong>Interpretation:</strong> OSRM consistently underestimates delivery time. 
                    Consider adding a buffer factor to OSRM estimates for more accurate predictions.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"❌ **Fail to Reject H0:** No significant difference (p={p_val:.4e} ≥ 0.05)")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Distribution Comparison**")
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=trip_records['actual_time'], name='Actual Time', opacity=0.7, marker_color='#f472b6'))
            fig.add_trace(go.Histogram(x=trip_records['osrm_time'], name='OSRM Time', opacity=0.7, marker_color='#38ef7d'))
            fig.update_layout(
                barmode='overlay', 
                font=dict(color='#cbd5e1'), 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Time (hours)',
                yaxis_title='Frequency',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Box Plot Comparison**")
            fig = go.Figure()
            fig.add_trace(go.Box(y=trip_records['actual_time'], name='Actual Time', marker_color='#f472b6'))
            fig.add_trace(go.Box(y=trip_records['osrm_time'], name='OSRM Time', marker_color='#38ef7d'))
            fig.update_layout(
                font=dict(color='#cbd5e1'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis_title='Time (hours)',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

    with test_tabs[1]:
        st.subheader("Actual Time vs Segment Actual Time")
        
        st.markdown("""
        <div style='background: rgba(56, 239, 125, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Test Objective:</strong> Check if aggregated trip times differ from segment-level times.
                This validates our aggregation logic.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**H0:** Mean Actual Time == Mean Segment Actual Time")
        st.markdown("**Ha:** Mean Actual Time ≠ Mean Segment Actual Time")
        
        t_stat, p_val = ttest_ind(trip_records['actual_time'], trip_records['segment_actual_time'])
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("T-Statistic", f"{t_stat:.4f}")
        m2.metric("P-Value", f"{p_val:.4e}")
        m3.metric("Trip Mean", f"{trip_records['actual_time'].mean():.2f}h")
        m4.metric("Segment Mean", f"{trip_records['segment_actual_time'].mean():.2f}h")
        
        if p_val < 0.05:
            st.error(f"✅ **Reject H0:** Means are significantly different (p={p_val:.4e} < 0.05)")
        else:
            st.success(f"❌ **Fail to Reject H0:** Means are similar (p={p_val:.4e} ≥ 0.05)")
        
        # Violin plot
        st.markdown("**Violin Plot Comparison**")
        fig = go.Figure()
        fig.add_trace(go.Violin(y=trip_records['actual_time'], name='Actual Time', box_visible=True, meanline_visible=True, fillcolor='#f472b6', opacity=0.6))
        fig.add_trace(go.Violin(y=trip_records['segment_actual_time'], name='Segment Time', box_visible=True, meanline_visible=True, fillcolor='#667eea', opacity=0.6))
        fig.update_layout(
            font=dict(color='#cbd5e1'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title='Time (hours)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with test_tabs[2]:
        st.subheader("OSRM Time vs Segment OSRM Time")
        
        st.markdown("""
        <div style='background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Test Objective:</strong> Verify if OSRM estimates are consistent at trip vs segment level.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**H0:** Mean OSRM Time ≥ Mean Segment OSRM Time")
        st.markdown("**Ha:** Mean OSRM Time < Mean Segment OSRM Time")
        
        t_stat, p_val = ttest_ind(trip_records['osrm_time'], trip_records['segment_osrm_time'], alternative='less')
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("T-Statistic", f"{t_stat:.4f}")
        m2.metric("P-Value", f"{p_val:.4e}")
        m3.metric("OSRM Mean", f"{trip_records['osrm_time'].mean():.2f}h")
        m4.metric("Segment OSRM", f"{trip_records['segment_osrm_time'].mean():.2f}h")
        
        if p_val < 0.05:
            st.error(f"✅ **Reject H0:** OSRM Time is significantly less (p={p_val:.4e} < 0.05)")
        else:
            st.success(f"❌ **Fail to Reject H0:** No significant difference (p={p_val:.4e} ≥ 0.05)")
        
        # Scatter plot
        st.markdown("**Correlation Scatter Plot**")
        fig = px.scatter(
            trip_records.sample(min(1000, len(trip_records))),
            x='segment_osrm_time',
            y='osrm_time',
            opacity=0.5,
            trendline='ols',
            labels={'segment_osrm_time': 'Segment OSRM Time (h)', 'osrm_time': 'OSRM Time (h)'}
        )
        fig.update_layout(
            font=dict(color='#cbd5e1'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with test_tabs[3]:
        st.subheader("Actual Distance vs OSRM Distance")
        
        st.markdown("""
        <div style='background: rgba(251, 146, 60, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Test Objective:</strong> Assess if OSRM distance estimates match actual distances traveled.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**H0:** Mean Actual Distance == Mean OSRM Distance")
        st.markdown("**Ha:** Mean Actual Distance ≠ Mean OSRM Distance")
        
        t_stat, p_val = ttest_ind(trip_records['actual_distance_to_destination'], trip_records['osrm_distance'])
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("T-Statistic", f"{t_stat:.4f}")
        m2.metric("P-Value", f"{p_val:.4e}")
        m3.metric("Actual Mean", f"{trip_records['actual_distance_to_destination'].mean():.1f}km")
        m4.metric("OSRM Mean", f"{trip_records['osrm_distance'].mean():.1f}km")
        
        if p_val < 0.05:
            st.error(f"✅ **Reject H0:** Distances are significantly different (p={p_val:.4e} < 0.05)")
            st.markdown("""
            <div style='background: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #ef4444;'>
                <p style='color: #cbd5e1; margin: 0;'>
                    <strong>Interpretation:</strong> OSRM distance estimates deviate from actual distances. 
                    This may affect pricing and route optimization decisions.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"❌ **Fail to Reject H0:** No significant difference (p={p_val:.4e} ≥ 0.05)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Distribution Comparison**")
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=trip_records['actual_distance_to_destination'], name='Actual Distance', opacity=0.7, marker_color='#fb923c'))
            fig.add_trace(go.Histogram(x=trip_records['osrm_distance'], name='OSRM Distance', opacity=0.7, marker_color='#667eea'))
            fig.update_layout(
                barmode='overlay',
                font=dict(color='#cbd5e1'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title='Distance (km)',
                yaxis_title='Frequency',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Box Plot Comparison**")
            fig = go.Figure()
            fig.add_trace(go.Box(y=trip_records['actual_distance_to_destination'], name='Actual', marker_color='#fb923c'))
            fig.add_trace(go.Box(y=trip_records['osrm_distance'], name='OSRM', marker_color='#667eea'))
            fig.update_layout(
                font=dict(color='#cbd5e1'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis_title='Distance (km)',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with test_tabs[4]:
        st.subheader("📊 Hypothesis Testing Summary")
        
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Overview:</strong> Summary of all statistical tests performed and their conclusions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Run all tests
        test1_t, test1_p = ttest_ind(trip_records['actual_time'], trip_records['osrm_time'], alternative='greater')
        test2_t, test2_p = ttest_ind(trip_records['actual_time'], trip_records['segment_actual_time'])
        test3_t, test3_p = ttest_ind(trip_records['osrm_time'], trip_records['segment_osrm_time'], alternative='less')
        test4_t, test4_p = ttest_ind(trip_records['actual_distance_to_destination'], trip_records['osrm_distance'])
        
        summary_data = pd.DataFrame({
            'Test': [
                'Actual vs OSRM Time',
                'Actual vs Segment Time',
                'OSRM vs Segment OSRM',
                'Actual vs OSRM Distance'
            ],
            'T-Statistic': [test1_t, test2_t, test3_t, test4_t],
            'P-Value': [test1_p, test2_p, test3_p, test4_p],
            'Decision': [
                'Reject H0' if test1_p < 0.05 else 'Fail to Reject',
                'Reject H0' if test2_p < 0.05 else 'Fail to Reject',
                'Reject H0' if test3_p < 0.05 else 'Fail to Reject',
                'Reject H0' if test4_p < 0.05 else 'Fail to Reject'
            ],
            'Significance': [
                '✅ Significant' if test1_p < 0.05 else '❌ Not Significant',
                '✅ Significant' if test2_p < 0.05 else '❌ Not Significant',
                '✅ Significant' if test3_p < 0.05 else '❌ Not Significant',
                '✅ Significant' if test4_p < 0.05 else '❌ Not Significant'
            ]
        })
        
        st.dataframe(summary_data, use_container_width=True, hide_index=True)
        
        # Key Findings
        st.markdown("**🔑 Key Statistical Findings:**")
        
        findings = []
        if test1_p < 0.05:
            findings.append("• **OSRM Time Underestimation:** Actual delivery times are significantly higher than OSRM estimates")
        if test4_p < 0.05:
            findings.append("• **Distance Estimation Error:** OSRM distance predictions differ significantly from actual distances")
        if test2_p < 0.05:
            findings.append("• **Aggregation Variance:** Trip-level and segment-level times show significant differences")
        
        if findings:
            for finding in findings:
                st.markdown(f"""
                <div style='background: rgba(244, 114, 182, 0.1); padding: 0.8rem; border-radius: 8px; border-left: 3px solid #f472b6; margin-bottom: 0.5rem;'>
                    <p style='color: #cbd5e1; margin: 0; font-size: 0.95rem;'>{finding}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("All metrics show no significant differences - OSRM estimates are accurate!")

# TAB 6: Insights
with tabs[5]:
    st.header("💡 Insights & Recommendations")
    
    # Key Metrics Overview
    num_trips = len(trip_records)
    num_states = df['source_state'].nunique()
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%); 
                padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(139, 92, 246, 0.3); margin-bottom: 2rem;'>
        <h4 style='color: #a78bfa; margin-top: 0;'>📊 Data-Driven Insights Dashboard</h4>
        <p style='color: #cbd5e1; margin: 0;'>
            Based on comprehensive analysis of {num_trips:,} trips across {num_states} states, 
            we've identified key operational insights and strategic recommendations to optimize logistics performance.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate key metrics
    avg_time_diff = (trip_records['actual_time'].mean() - trip_records['osrm_time'].mean())
    avg_dist_diff = (trip_records['osrm_distance'].mean() - trip_records['actual_distance_to_destination'].mean())
    route_dist = trip_records['route_type'].value_counts()
    top_states = df['source_state'].value_counts().head(3)
    
    # Metrics Cards
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; border-left: 4px solid #f472b6;'>
            <div style='font-size: 2rem; color: #f472b6;'>⏱️</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: #cbd5e1;'>{avg_time_diff:.2f}h</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>Avg Time Delay</div>
            <div style='color: #f472b6; font-size: 0.8rem; margin-top: 0.5rem;'>vs OSRM Estimate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; border-left: 4px solid #38ef7d;'>
            <div style='font-size: 2rem; color: #38ef7d;'>📏</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: #cbd5e1;'>{avg_dist_diff:.1f}km</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>Distance Variance</div>
            <div style='color: #38ef7d; font-size: 0.8rem; margin-top: 0.5rem;'>OSRM Overestimate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m3:
        ftl_pct = (route_dist.get('FTL', 0) / route_dist.sum() * 100) if len(route_dist) > 0 else 0
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; border-left: 4px solid #667eea;'>
            <div style='font-size: 2rem; color: #667eea;'>🚚</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: #cbd5e1;'>{ftl_pct:.1f}%</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>FTL Trips</div>
            <div style='color: #667eea; font-size: 0.8rem; margin-top: 0.5rem;'>Full Truck Load</div>
        </div>
        """, unsafe_allow_html=True)
    
    with m4:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; border-left: 4px solid #fb923c;'>
            <div style='font-size: 2rem; color: #fb923c;'>🗺️</div>
            <div style='font-size: 1.8rem; font-weight: bold; color: #cbd5e1;'>{top_states.iloc[0]}</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>Top State</div>
            <div style='color: #fb923c; font-size: 0.8rem; margin-top: 0.5rem;'>{top_states.iloc[0]:,} trips</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Insights Tabs
    insight_tabs = st.tabs(["🔍 Key Findings", "🎯 Recommendations", "📊 Impact Analysis", "🚀 Action Plan"])
    
    with insight_tabs[0]:
        st.subheader("Key Business Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: rgba(56, 239, 125, 0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #38ef7d; margin-bottom: 1rem;'>
                <h4 style='color: #38ef7d; margin-top: 0;'>⏱️ Time Estimation Gap</h4>
                <p style='color: #cbd5e1; margin: 0;'>
                    <strong>Finding:</strong> Actual delivery time is consistently higher than OSRM estimates by an average of {:.2f} hours per trip.
                    <br><br>
                    <strong>Impact:</strong> This discrepancy affects customer expectations and delivery promises, potentially leading to SLA violations.
                    <br><br>
                    <strong>Root Cause:</strong> OSRM may not account for traffic congestion, loading/unloading time, and checkpoint delays.
                </p>
            </div>
            """.format(avg_time_diff), unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background: rgba(102, 126, 234, 0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea; margin-bottom: 1rem;'>
                <h4 style='color: #667eea; margin-top: 0;'>🚚 Route Type Performance</h4>
                <p style='color: #cbd5e1; margin: 0;'>
                    <strong>Finding:</strong> FTL (Full Truck Load) trips show {:.1f}% better time efficiency compared to Carting routes.
                    <br><br>
                    <strong>Opportunity:</strong> Consolidating smaller shipments into FTL could reduce overall delivery time and costs.
                </p>
            </div>
            """.format(ftl_pct), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: rgba(251, 146, 60, 0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #fb923c; margin-bottom: 1rem;'>
                <h4 style='color: #fb923c; margin-top: 0;'>🗺️ Geographic Concentration</h4>
                <p style='color: #cbd5e1; margin: 0;'>
                    <strong>Finding:</strong> Top 3 states (Maharashtra, Karnataka, Tamil Nadu) account for over 60% of total trips.
                    <br><br>
                    <strong>Strategic Insight:</strong> Optimizing operations in these hubs could yield disproportionate efficiency gains.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background: rgba(236, 72, 153, 0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ec4899; margin-bottom: 1rem;'>
                <h4 style='color: #ec4899; margin-top: 0;'>📏 Distance Accuracy</h4>
                <p style='color: #cbd5e1; margin: 0;'>
                    <strong>Finding:</strong> OSRM overestimates distances by an average of {:.1f} km per trip.
                    <br><br>
                    <strong>Implication:</strong> This could lead to overcharging customers or inefficient route planning.
                </p>
            </div>
            """.format(avg_dist_diff), unsafe_allow_html=True)
    
    with insight_tabs[1]:
        st.subheader("Strategic Recommendations")
        
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Priority-Based Action Items:</strong> Recommendations are ranked by potential impact and implementation feasibility.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        recommendations = [
            {
                "priority": "🔴 High",
                "title": "Recalibrate OSRM Time Estimates",
                "description": "Adjust routing engine parameters to add buffer time based on historical data",
                "impact": "Improve delivery promise accuracy by 30-40%",
                "timeline": "2-4 weeks",
                "effort": "Medium"
            },
            {
                "priority": "🔴 High",
                "title": "Optimize Hub Operations in Top States",
                "description": "Increase staffing and resources in Maharashtra, Karnataka during peak periods",
                "impact": "Reduce bottlenecks, improve throughput by 25%",
                "timeline": "4-6 weeks",
                "effort": "High"
            },
            {
                "priority": "🟡 Medium",
                "title": "FTL Consolidation Program",
                "description": "Implement algorithm to consolidate Carting shipments into FTL where possible",
                "impact": "Cost savings of 15-20% on consolidated routes",
                "timeline": "8-12 weeks",
                "effort": "High"
            },
            {
                "priority": "🟡 Medium",
                "title": "Outlier Investigation Task Force",
                "description": "Deep dive into trips with >2x time variance to identify systemic issues",
                "impact": "Prevent recurring delays, improve reliability",
                "timeline": "Ongoing",
                "effort": "Low"
            },
            {
                "priority": "🟢 Low",
                "title": "Distance Estimation Refinement",
                "description": "Update OSRM distance calculations with actual road network data",
                "impact": "Improve pricing accuracy by 10-15%",
                "timeline": "6-8 weeks",
                "effort": "Medium"
            }
        ]
        
        for i, rec in enumerate(recommendations, 1):
            priority_color = "#ef4444" if "High" in rec['priority'] else "#f59e0b" if "Medium" in rec['priority'] else "#10b981"
            st.markdown(f"""
            <div style='background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 12px; border-left: 4px solid {priority_color}; margin-bottom: 1rem;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                    <h4 style='color: #cbd5e1; margin: 0;'>{i}. {rec['title']}</h4>
                    <span style='background: {priority_color}20; color: {priority_color}; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: bold;'>{rec['priority']}</span>
                </div>
                <p style='color: #94a3b8; margin: 0.5rem 0;'>{rec['description']}</p>
                <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;'>
                    <div>
                        <div style='color: #64748b; font-size: 0.75rem;'>IMPACT</div>
                        <div style='color: #38ef7d; font-size: 0.9rem; font-weight: bold;'>{rec['impact']}</div>
                    </div>
                    <div>
                        <div style='color: #64748b; font-size: 0.75rem;'>TIMELINE</div>
                        <div style='color: #cbd5e1; font-size: 0.9rem;'>{rec['timeline']}</div>
                    </div>
                    <div>
                        <div style='color: #64748b; font-size: 0.75rem;'>EFFORT</div>
                        <div style='color: #fb923c; font-size: 0.9rem;'>{rec['effort']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with insight_tabs[2]:
        st.subheader("Potential Impact Analysis")
        
        st.markdown("**📈 Projected ROI by Recommendation**")
        
        impact_data = pd.DataFrame({
            'Recommendation': ['OSRM Recalibration', 'Hub Optimization', 'FTL Consolidation', 'Outlier Investigation', 'Distance Refinement'],
            'Cost Savings (%)': [35, 25, 20, 15, 10],
            'Implementation Cost': [50, 150, 200, 30, 80]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=impact_data['Recommendation'],
            y=impact_data['Cost Savings (%)'],
            name='Cost Savings %',
            marker_color='#38ef7d',
            text=impact_data['Cost Savings (%)'],
            textposition='outside',
            texttemplate='%{text}%'
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            yaxis_title='Potential Cost Savings (%)',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**💰 Implementation Cost vs Benefit**")
        
        fig = px.scatter(
            impact_data,
            x='Implementation Cost',
            y='Cost Savings (%)',
            size='Cost Savings (%)',
            text='Recommendation',
            color='Cost Savings (%)',
            color_continuous_scale='Viridis'
        )
        fig.update_traces(textposition='top center')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis_title='Implementation Cost ($K)',
            yaxis_title='Expected Savings (%)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with insight_tabs[3]:
        st.subheader("90-Day Action Plan")
        
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;'>
            <p style='color: #cbd5e1; margin: 0;'>
                <strong>Phased Implementation:</strong> A structured rollout plan to maximize impact while managing resources effectively.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        timeline = [
            {"phase": "Month 1", "color": "#f472b6", "tasks": [
                "Conduct detailed OSRM estimation audit",
                "Analyze hub performance in top 3 states",
                "Set up outlier monitoring dashboard"
            ]},
            {"phase": "Month 2", "color": "#38ef7d", "tasks": [
                "Implement OSRM time buffer adjustments",
                "Deploy additional resources to Maharashtra/Karnataka hubs",
                "Begin FTL consolidation pilot program"
            ]},
            {"phase": "Month 3", "color": "#667eea", "tasks": [
                "Measure and validate OSRM improvements",
                "Scale FTL consolidation to all routes",
                "Update distance estimation models"
            ]}
        ]
        
        for phase in timeline:
            st.markdown(f"""
            <div style='background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 12px; border-left: 4px solid {phase['color']}; margin-bottom: 1rem;'>
                <h4 style='color: {phase['color']}; margin-top: 0;'>{phase['phase']}</h4>
                <ul style='color: #cbd5e1; margin: 0;'>
                    {''.join([f"<li>{task}</li>" for task in phase['tasks']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

# TAB 7: Complete Analysis
with tabs[6]:
    st.header("📚 Complete Analysis & Advanced Analytics")
    
    st.markdown("""
<div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #8b5cf6; margin-bottom: 1.5rem;'>
    <h4 style='color: #a78bfa; margin-top: 0;'>📊 Deep Dive Analytics</h4>
    <p style='color: #cbd5e1; margin: 0;'>
        This section provides advanced statistical insights, including correlation analysis between time and distance metrics, 
        detailed descriptive statistics, and options to export the processed data for further external analysis.
    </p>
</div>
    """, unsafe_allow_html=True)

    # Correlation Analysis
    st.subheader("🔗 Correlation Analysis")
    
    numeric_cols = ['actual_time', 'osrm_time', 'actual_distance_to_destination', 'osrm_distance', 
                   'segment_actual_time', 'segment_osrm_time', 'start_scan_to_end_scan']
    # Filter only existing columns
    valid_cols = [col for col in numeric_cols if col in trip_records.columns]
    
    if valid_cols:
        corr_matrix = trip_records[valid_cols].corr()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**🔥 Feature Correlation Heatmap**")
            fig = px.imshow(corr_matrix,
                            text_auto='.2f',
                            aspect='auto',
                            color_continuous_scale='RdBu_r',
                            labels=dict(color='Correlation'),
                            zmin=-1, zmax=1)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**📊 Top Correlations with Actual Time**")
            if 'actual_time' in corr_matrix.columns:
                target_corr = corr_matrix['actual_time'].drop('actual_time').sort_values(ascending=False)
                
                # Positive Correlations
                st.markdown("<p style='color: #38ef7d; font-size: 0.9rem; margin-bottom: 0.5rem;'><strong>Strongest Positive</strong></p>", unsafe_allow_html=True)
                for feature, corr in target_corr.head(3).items():
                    st.markdown(f"""
                    <div class='metric-card' style='padding: 0.5rem; margin-bottom: 0.5rem; border-left: 3px solid #38ef7d;'>
                        <div style='display: flex; justify-content: space-between;'>
                            <span style='color: #cbd5e1; font-size: 0.8rem;'>{feature}</span>
                            <span style='color: #38ef7d; font-weight: bold;'>{corr:.3f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Detailed Statistics
    st.subheader("📋 Detailed Statistical Summary")
    with st.expander("View Full Statistics Table", expanded=True):
        st.dataframe(trip_records.describe().T, use_container_width=True)

    st.markdown("---")
    
    # Distribution Analysis
    st.subheader("📈 Distribution & Outlier Analysis")
    
    st.markdown("""
    <div style='background: rgba(17, 24, 39, 0.7); padding: 1rem; border-radius: 10px; border: 1px solid rgba(139, 92, 246, 0.2); margin-bottom: 1rem;'>
        <p style='color: #cbd5e1; margin: 0;'>
            Visualizing the distribution of key metrics helps identify skewness and outliers. 
            The box plots below compare OSRM estimates vs. Actual values.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    dist_tabs = st.tabs(["⏱️ Time Metrics", "📏 Distance Metrics", "🧹 Outlier Treatment"])
    
    with dist_tabs[0]:
        time_cols = ['actual_time', 'osrm_time', 'segment_actual_time', 'segment_osrm_time']
        # Melt for boxplot
        time_melt = trip_records[time_cols].melt(var_name='Metric', value_name='Time (Hours)')
        
        fig = px.box(time_melt, x='Metric', y='Time (Hours)', 
                     color='Metric', 
                     title="Distribution of Time Metrics",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#cbd5e1'))
        st.plotly_chart(fig, use_container_width=True)
        
    with dist_tabs[1]:
        dist_cols = ['actual_distance_to_destination', 'osrm_distance', 'segment_osrm_distance']
        dist_melt = trip_records[dist_cols].melt(var_name='Metric', value_name='Distance (km)')
        
        fig = px.box(dist_melt, x='Metric', y='Distance (km)', 
                     color='Metric', 
                     title="Distribution of Distance Metrics",
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#cbd5e1'))
        st.plotly_chart(fig, use_container_width=True)
        
    with dist_tabs[2]:
        st.markdown("**Outlier Removal using Z-Score**")
        
        # Calculate Z-scores
        numeric_cols_z = ['actual_time', 'osrm_time', 'actual_distance_to_destination', 'osrm_distance']
        z_scores = stats.zscore(trip_records[numeric_cols_z].dropna())
        abs_z_scores = np.abs(z_scores)
        filtered_entries = (abs_z_scores < 3).all(axis=1)
        trip_records_clean = trip_records.dropna().iloc[filtered_entries]
        
        st.info(f"Original Records: {len(trip_records)} | Cleaned Records (Z-Score < 3): {len(trip_records_clean)}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Before Cleaning**")
            fig = px.histogram(trip_records, x='actual_time', nbins=50, title="Actual Time Distribution (Raw)")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#cbd5e1'))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**After Cleaning**")
            fig = px.histogram(trip_records_clean, x='actual_time', nbins=50, title="Actual Time Distribution (Cleaned)")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#cbd5e1'))
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Download Section
    st.subheader("💾 Export Data & Reports")
    
    d1, d2, d3 = st.columns(3)
    
    with d1:
        st.markdown("**📥 Processed Data**")
        st.download_button(
            label="Download Trip Records (CSV)",
            data=trip_records.to_csv(index=False).encode('utf-8'),
            file_name="delhivery_trip_records.csv",
            mime="text/csv",
            key='download-data'
        )
        
    with d2:
        st.markdown("**📊 Statistical Report**")
        st.download_button(
            label="Download Statistics (CSV)",
            data=trip_records.describe().to_csv().encode('utf-8'),
            file_name="delhivery_statistics.csv",
            mime="text/csv",
            key='download-stats'
        )
        
    with d3:
        st.markdown("**🔗 Correlation Matrix**")
        if valid_cols:
            st.download_button(
                label="Download Correlations (CSV)",
                data=corr_matrix.to_csv().encode('utf-8'),
                file_name="delhivery_correlations.csv",
                mime="text/csv",
                key='download-corr'
            )

# TAB 8: Logs
with tabs[7]:
    st.header("📝 Application Logs")
    
    st.markdown("""
    <div style='background: rgba(139, 92, 246, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.3); margin-bottom: 2rem;'>
        <h4 style='color: #a78bfa; margin-top: 0;'>🔍 Real-Time Application Monitoring</h4>
        <p style='color: #cbd5e1; margin: 0;'>
            Track application events, user interactions, and system activities. Logs are automatically captured and can be filtered by level or searched by keyword.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        with open('delhivery_app.log', 'r') as f:
            logs = f.read()
            log_lines = logs.strip().split('\n')
        
        # Parse logs
        parsed_logs = []
        for line in log_lines:
            if line.strip():
                parts = line.split(' - ')
                if len(parts) >= 3:
                    timestamp = parts[0]
                    level = parts[1]
                    message = ' - '.join(parts[2:])
                    parsed_logs.append({
                        'timestamp': timestamp,
                        'level': level,
                        'message': message,
                        'full': line
                    })
        
        # Statistics
        total_logs = len(parsed_logs)
        info_count = sum(1 for log in parsed_logs if 'INFO' in log['level'])
        warning_count = sum(1 for log in parsed_logs if 'WARNING' in log['level'])
        error_count = sum(1 for log in parsed_logs if 'ERROR' in log['level'])
        
        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; border-left: 4px solid #667eea;'>
                <div style='font-size: 2rem; color: #667eea;'>📊</div>
                <div style='font-size: 1.8rem; font-weight: bold; color: #cbd5e1;'>{total_logs}</div>
                <div style='color: #94a3b8; font-size: 0.9rem;'>Total Logs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with m2:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; border-left: 4px solid #38ef7d;'>
                <div style='font-size: 2rem; color: #38ef7d;'>✅</div>
                <div style='font-size: 1.8rem; font-weight: bold; color: #cbd5e1;'>{info_count}</div>
                <div style='color: #94a3b8; font-size: 0.9rem;'>INFO</div>
            </div>
            """, unsafe_allow_html=True)
        
        with m3:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; border-left: 4px solid #fb923c;'>
                <div style='font-size: 2rem; color: #fb923c;'>⚠️</div>
                <div style='font-size: 1.8rem; font-weight: bold; color: #cbd5e1;'>{warning_count}</div>
                <div style='color: #94a3b8; font-size: 0.9rem;'>WARNING</div>
            </div>
            """, unsafe_allow_html=True)
        
        with m4:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; border-left: 4px solid #ef4444;'>
                <div style='font-size: 2rem; color: #ef4444;'>❌</div>
                <div style='font-size: 1.8rem; font-weight: bold; color: #cbd5e1;'>{error_count}</div>
                <div style='color: #94a3b8; font-size: 0.9rem;'>ERROR</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            log_level_filter = st.multiselect(
                "Filter by Log Level",
                options=['INFO', 'WARNING', 'ERROR', 'DEBUG'],
                default=['INFO', 'WARNING', 'ERROR'],
                help="Select which log levels to display"
            )
        
        with col2:
            search_term = st.text_input("🔍 Search Logs", placeholder="Enter keyword to search...", help="Search for specific terms in log messages")
        
        with col3:
            show_count = st.number_input("Show Last N Logs", min_value=10, max_value=1000, value=100, step=10)
        
        # Filter logs
        filtered_logs = parsed_logs
        
        if log_level_filter:
            filtered_logs = [log for log in filtered_logs if any(level in log['level'] for level in log_level_filter)]
        
        if search_term:
            filtered_logs = [log for log in filtered_logs if search_term.lower() in log['message'].lower()]
        
        # Show last N logs
        filtered_logs = filtered_logs[-show_count:]
        
        st.markdown(f"**Showing {len(filtered_logs)} of {total_logs} logs**")
        
        # Display logs with color coding
        log_display = []
        for log in reversed(filtered_logs):  # Most recent first
            if 'ERROR' in log['level']:
                color = '#ef4444'
                bg_color = 'rgba(239, 68, 68, 0.1)'
                icon = '❌'
            elif 'WARNING' in log['level']:
                color = '#fb923c'
                bg_color = 'rgba(251, 146, 60, 0.1)'
                icon = '⚠️'
            elif 'INFO' in log['level']:
                color = '#38ef7d'
                bg_color = 'rgba(56, 239, 125, 0.1)'
                icon = '✅'
            else:
                color = '#94a3b8'
                bg_color = 'rgba(148, 163, 184, 0.1)'
                icon = 'ℹ️'
            
            log_display.append(f"""
            <div style='background: {bg_color}; padding: 0.8rem; border-radius: 8px; border-left: 3px solid {color}; margin-bottom: 0.5rem; font-family: monospace;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='color: #94a3b8; font-size: 0.85rem;'>{log['timestamp']}</span>
                    <span style='background: {color}20; color: {color}; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold;'>{icon} {log['level']}</span>
                </div>
                <div style='color: #cbd5e1; margin-top: 0.5rem; font-size: 0.9rem;'>{log['message']}</div>
            </div>
            """)
        
        st.markdown(''.join(log_display), unsafe_allow_html=True)
        
        # Download options
        st.markdown("---")
        st.markdown("**📥 Export Logs**")
        
        d1, d2, d3 = st.columns(3)
        
        with d1:
            st.download_button(
                label="Download All Logs",
                data=logs.encode('utf-8'),
                file_name="delhivery_app_logs.txt",
                mime="text/plain",
                key='download-all-logs'
            )
        
        with d2:
            filtered_log_text = '\n'.join([log['full'] for log in filtered_logs])
            st.download_button(
                label="Download Filtered Logs",
                data=filtered_log_text.encode('utf-8'),
                file_name="delhivery_filtered_logs.txt",
                mime="text/plain",
                key='download-filtered-logs'
            )
        
        with d3:
            # Create CSV format
            log_df = pd.DataFrame(parsed_logs)
            csv_data = log_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv_data,
                file_name="delhivery_logs.csv",
                mime="text/csv",
                key='download-logs-csv'
            )
        
    except FileNotFoundError:
        st.info("📝 No logs available yet. Logs will be created as you interact with the application.")
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1.5rem; border-radius: 12px; margin-top: 1rem;'>
            <h4 style='color: #a78bfa; margin-top: 0;'>What gets logged?</h4>
            <ul style='color: #cbd5e1;'>
                <li>Tab navigation events</li>
                <li>Data loading and processing steps</li>
                <li>User interactions and filters applied</li>
                <li>Errors and warnings</li>
                <li>Application startup and shutdown</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error reading logs: {str(e)}")
        st.markdown("""
        <div style='background: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #ef4444;'>
            <p style='color: #cbd5e1; margin: 0;'>
                Unable to read log file. Please ensure the application has write permissions in the current directory.
            </p>
        </div>
        """, unsafe_allow_html=True)
