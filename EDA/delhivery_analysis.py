"""
Delhivery Feature Engineering Analysis
Converted from: Delhivery Final.ipynb
"""


# ================================================================================
# MARKDOWN CELL 1
# ================================================================================
# 
# # About Delhivery : 
# 
# - Delhivery is the largest and fastest-growing fully integrated player in India by revenue in Fiscal 2021. They aim to build the operating system for commerce, through a combination of world-class infrastructure, logistics operations of the highest quality, and cutting-edge engineering and technology capabilities.
# 
# 
# - The Data team builds intelligence and capabilities using this data that helps them to widen the gap between the quality, efficiency, and profitability of their business versus their competitors.
# 
# 
# # Business Problem Statement  :
# 
# 
# - The company wants to understand and process the data coming out of data engineering pipelines:
# 
# >• Clean, sanitize and manipulate data to get useful features out of raw fields
# 
# >• Make sense out of the raw data and help the data science team to build forecasting models on it.
# 
# 
# ### Column Profiling:
# 
# - data :  tells whether the data is testing or training data
# 
# 
# - trip_creation_time : Timestamp of trip creation
# - route_schedule_uuid : Unique Id for a particular route schedule
# - route_type : Transportation type 
#     - FTL – Full Truck Load: FTL shipments get to the destination sooner, as the truck is making no other pickups or drop-offs along the way
#     - Carting: Handling system consisting of small vehicles (carts)
#     
# - trip_uuid : Unique ID given to a particular trip (A trip may include different source and destination centers)
# - source_center : Source ID of trip origin
# - source_name : Source Name of trip origin
# - destination_cente : Destination ID
# - destination_name : Destination Name
# - od_start_time : Trip start time
# - od_end_time : Trip end time
# - start_scan_to_end_scan : Time taken to deliver from source to destination
# - is_cutoff : Unknown field
# - cutoff_factor : Unknown field
# - cutoff_timestamp : Unknown field
# - actual_distance_to_destination : Distance in Kms between source and destination warehouse
# - actual_time : Actual time taken to complete the delivery (Cumulative)
# - osrm_time : An open-source routing engine time calculator which computes the shortest path between points in a given map (Includes usual traffic, distance through major and minor roads) and gives the time (Cumulative)
# - osrm_distance : An open-source routing engine which computes the shortest path between points in a given map (Includes usual traffic, distance through major and minor roads) (Cumulative)
# - factor : Unknown field
# - segment_actual_time : This is a segment time. Time taken by the subset of the package delivery
# - segment_osrm_time : This is the OSRM segment time. Time taken by the subset of the package delivery
# - segment_osrm_distance : This is the OSRM distance. Distance covered by subset of the package delivery
# - segment_factor : Unknown field
# 
# 
# 
# 
# 
# - #### In-depth analysis and feature engineering to be done : 
#     
#     > - time taken between od_start_time and od_end_time 
#     
#     > - hypothesis testing/ Visual analysis : population mean of start_scan_to_end_scan & time taken between od_start_time and od_end_time
#     > - hypothesis testing/ visual analysis :
#             - actual_time aggregated value and OSRM time aggregated value 
#             
#     > - hypothesis testing/ visual analysis :
#             - actual_time aggregated value and segment actual time 
#             
#     > - hypothesis testing/ visual analysis : 
#             - osrm distance aggregated value and segment osrm distance 
#             
#     > - hypothesis testing/ visual analysis :
#             - osrm time aggregated value and segment osrm time aggregated value
#             
#             
#     > - outliers in the numerical variables 
#     
#     > - outliers using the IQR method.
#     
#     > - one-hot encoding of categorical variables (like route_type)
#     
#     > - Normalize/ Standardize the numerical features using MinMaxScaler or StandardScaler.
# 
# 


# ================================================================================
# CODE CELL 2
# ================================================================================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
from matplotlib import figure
import warnings
warnings.filterwarnings('ignore')
import statsmodels.api as sm
from scipy.stats import norm
from scipy.stats import t
import plotly.express as px


# ================================================================================
# CODE CELL 3
# ================================================================================

pd.set_option('display.max_columns', None)


# ================================================================================
# CODE CELL 4
# ================================================================================




# ================================================================================
# CODE CELL 5
# ================================================================================

df = pd.read_csv("delhivery_data.txt")


# ================================================================================
# CODE CELL 6
# ================================================================================

df.head(5)


# ================================================================================
# MARKDOWN CELL 7
# ================================================================================
# # Understanding shape and structure of data : 


# ================================================================================
# CODE CELL 8
# ================================================================================

df.shape


# ================================================================================
# CODE CELL 9
# ================================================================================

# 144,867 total Records 
# 24 columns 


# ================================================================================
# CODE CELL 10
# ================================================================================

df.info()


# ================================================================================
# CODE CELL 11
# ================================================================================

df.isna().sum()


# ================================================================================
# CODE CELL 12
# ================================================================================

# features : source_name and destination_name having few missing values


# ================================================================================
# MARKDOWN CELL 13
# ================================================================================
# ## Changing data type for data and time related features : 
# 


# ================================================================================
# CODE CELL 14
# ================================================================================

df["od_end_time"] = pd.to_datetime(df["od_end_time"])
df["od_start_time"] = pd.to_datetime(df["od_start_time"])
df["trip_creation_time"] = pd.to_datetime(df["trip_creation_time"])


# ================================================================================
# MARKDOWN CELL 15
# ================================================================================
# ## Extracting Trip Creation Informations from Trip Creation time : 


# ================================================================================
# CODE CELL 16
# ================================================================================

df["trip_creation_time"].dt.month_name().value_counts()


# ================================================================================
# CODE CELL 17
# ================================================================================

df["trip_creation_time"].dt.year.value_counts()


# ================================================================================
# CODE CELL 18
# ================================================================================

# delivery trip data is given from Septemebr and October 2018.


# ================================================================================
# CODE CELL 19
# ================================================================================

df["trip_creation_day"] = (df["trip_creation_time"].dt.day_name())
df["trip_creation_month"] = (df["trip_creation_time"].dt.month_name())
df["trip_creation_year"] = (df["trip_creation_time"].dt.year)


# ================================================================================
# CODE CELL 20
# ================================================================================

df["trip_creation_day"].value_counts().plot(kind = "bar")


# ================================================================================
# CODE CELL 21
# ================================================================================

# wednesday seems to have relatively higher records of data compare to other days . 
df["trip_creation_day"].value_counts(normalize=True)*100


# ================================================================================
# CODE CELL 22
# ================================================================================




# ================================================================================
# MARKDOWN CELL 23
# ================================================================================
# # Understanding the structure : 


# ================================================================================
# CODE CELL 24
# ================================================================================

df.nunique()


# ================================================================================
# MARKDOWN CELL 25
# ================================================================================
# ### we have `14817 different trips happended between source to destinations.` 
# ### total ` 1504 delivery routes` we have.
# 
# #### 1508 unique source centers 
# #### 1481 unique destination centres 
# 
# 
# ## There are two different kind of routes are there : 


# ================================================================================
# CODE CELL 26
# ================================================================================

df.groupby("trip_uuid")["route_type"].unique().reset_index()["route_type"].apply(lambda x:x[0]).value_counts()


# ================================================================================
# CODE CELL 27
# ================================================================================

df.groupby("trip_uuid")["route_type"].unique().reset_index()["route_type"].apply(lambda x:x[0]).value_counts(normalize = True)*100


# ================================================================================
# CODE CELL 28
# ================================================================================

routeType_plot= (df.groupby("trip_uuid")["route_type"].unique().reset_index()["route_type"].apply(lambda x:x[0]).value_counts(normalize = True)*100)
routeType_plot


# ================================================================================
# CODE CELL 29
# ================================================================================

sns.barplot(x= routeType_plot.index,
           y = routeType_plot)


# ================================================================================
# MARKDOWN CELL 30
# ================================================================================
# #### From `14817 total different trips` , we have 
# #### 8908 `(60%)` of the trip-routes are `Carting` , which consists of small vehicles and 
# #### 5909 `(40%)` of total trip-routes are `FTL` : which are Full Truck Load get to the destination sooner.  as no otther pickups  or drop offs along the way . 


# ================================================================================
# CODE CELL 31
# ================================================================================




# ================================================================================
# CODE CELL 32
# ================================================================================




# ================================================================================
# CODE CELL 33
# ================================================================================




# ================================================================================
# MARKDOWN CELL 34
# ================================================================================
# # Undestanding Features and Feature Engineering  :
# 
# ## Analyzing records for one particular trip id : 
# 


# ================================================================================
# CODE CELL 35
# ================================================================================

df[df["trip_uuid"]=="trip-153741093647649320"]


# ================================================================================
# MARKDOWN CELL 36
# ================================================================================
#     from above one particular trip record , 
#     trip is segmented between different drop locations .
# 
#     we can observe 
#     trip is taking stops between mentioned source and destination centers(warehouses).
#     od-end-tiem and od-start-time are the time when the that particular trip was ended and started .
# 
#     start-scan-to-end-scan is the time duration of trips are being scanned when start and end. 
#     start-scan-to-end-scan time is given cummulative. which is not given per trip segments.
# 
# 
#     trip cut off False ,shows the record of trip when trip changes from one warehouse to another. between source to destination. 
# 
# 
#     Actual-time given is the time to complete the entire delivery from source to destination (given cumulatively )
# 
# 
# 
# 
#     osrm -time is an open rourse routing engine time calculator which computes the shortest path between points in a given map and gives the time and osrm distance gives the shortest distance (given cumulatively )
# 
# 
#     Actual-distnace-to-destination is the actual distance between warehouses , given cummulative during the trip . 
#     every time cutoff is False , distance count starts from begining. 
# 
#     Segmment actual time,  is the actual time taken between two stops in between trips. given per each segment (taken between subset of package delivery)
# 
#     segment osrm time is the osrm segment time , taken between subset of package delivery
# 
# 
# 


# ================================================================================
# MARKDOWN CELL 37
# ================================================================================
# ### Extracting Features like city - place - code -state from source and destination name columns : 


# ================================================================================
# CODE CELL 38
# ================================================================================

df["source_city"] = df["source_name"].str.split(" ",n=1,expand=True)[0].str.split("_",n=1,expand=True)[0]
df["source_state"] = df["source_name"].str.split(" ",n=1,expand=True)[1].str.replace("(","").str.replace(")","")

df["destination_city"] = df["destination_name"].str.split(" ",n=1,expand=True)[0].str.split("_",n=1,expand=True)[0]
df["destination_state"] = df["destination_name"].str.split(" ",n=1,expand=True)[1].str.replace("(","").str.replace(")","")


# ================================================================================
# CODE CELL 39
# ================================================================================

df["source_place"] = df["source_name"].str.split("_",n=2,expand=True)[1]
df["destination_place"] = df["destination_name"].str.split("_",n=2,expand=True)[1]



# ================================================================================
# CODE CELL 40
# ================================================================================




# ================================================================================
# CODE CELL 41
# ================================================================================

df["source_pincode"] = df["source_center"].apply(lambda x : x[3:9] )
df["destination_pincode"] = df["destination_center"].apply(lambda x : x[3:9] )


# ================================================================================
# CODE CELL 42
# ================================================================================

df


# ================================================================================
# MARKDOWN CELL 43
# ================================================================================
# 
# ####  Time_taken_btwn_odstart_and_od_end VS start_scan_to_end_scan : 


# ================================================================================
# CODE CELL 44
# ================================================================================

df["time_taken_btwn_odstart_and_od_end"] = ((df["od_end_time"]-df["od_start_time"])/pd.Timedelta(1,unit="hour"))


# ================================================================================
# MARKDOWN CELL 45
# ================================================================================
# #### Converting given time duration features into hours . 
#     start_scan_to_end_scan
#     actual_time
#     osrm_time
#     segment_actual_time
#     segment_osrm_time
#     


# ================================================================================
# MARKDOWN CELL 46
# ================================================================================
# 


# ================================================================================
# CODE CELL 47
# ================================================================================

df["start_scan_to_end_scan"] = df["start_scan_to_end_scan"]/60
df["actual_time"] = df["actual_time"]/60
df["osrm_time"] = df["osrm_time"]/60
df["segment_actual_time"] = df["segment_actual_time"]/60
df["segment_osrm_time"] = df["segment_osrm_time"]/60


# ================================================================================
# CODE CELL 48
# ================================================================================

df


# ================================================================================
# CODE CELL 49
# ================================================================================

df.info()


# ================================================================================
# CODE CELL 50
# ================================================================================

df.isna().sum()


# ================================================================================
# CODE CELL 51
# ================================================================================

df.shape


# ================================================================================
# MARKDOWN CELL 52
# ================================================================================
# ## Data cleaning : 


# ================================================================================
# CODE CELL 53
# ================================================================================

df["source_state"] = df["source_state"].replace({"Goa Goa":"Goa",
                           "Layout PC Karnataka":"Karnataka",
                           "Vadgaon Sheri DPC Maharashtra":"Maharashtra",
                           "Pashan DPC Maharashtra":"Maharashtra",
                           "City Madhya Pradesh":"Madhya Pradesh",
                           "02_DPC Uttar Pradesh":"Uttar Pradesh",
                           "Nagar_DC Rajasthan":"Rajasthan",
                           "Alipore_DPC West Bengal":"West Bengal",
                            "Mandakni Madhya Pradesh":"Madhya Pradesh",
                            "West _Dc Maharashtra":"Maharashtra",
                            "DC Rajasthan":"Rajasthan",
                            "MP Nagar Madhya Pradesh":"Madhya Pradesh",
                            "Antop Hill Maharashtra":"Maharashtra",
                            "Avenue_DPC West Bengal":"West Bengal",
                            "Nagar Uttar Pradesh":"Uttar Pradesh",
                            "Balaji Nagar Maharashtra":"Maharashtra",
                            "Kothanur_L Karnataka":"Karnataka",
                            "Rahatani DPC Maharashtra":"Maharashtra",
                            "Mahim Maharashtra":"Maharashtra",
                            "DC Maharashtra":"Maharashtra",
                            "_NAD Andhra Pradesh":"Andhra Pradesh",
                                                       })


# ================================================================================
# CODE CELL 54
# ================================================================================

df["destination_state"] = df["destination_state"].replace({"Goa Goa":"Goa",
                           "Layout PC Karnataka":"Karnataka",
                           "Vadgaon Sheri DPC Maharashtra":"Maharashtra",
                           "Pashan DPC Maharashtra":"Maharashtra",
                           "City Madhya Pradesh":"Madhya Pradesh",
                           "02_DPC Uttar Pradesh":"Uttar Pradesh",
                           "Nagar_DC Rajasthan":"Rajasthan",
                           "Alipore_DPC West Bengal":"West Bengal",
                            "Mandakni Madhya Pradesh":"Madhya Pradesh",
                            "West _Dc Maharashtra":"Maharashtra",
                            "DC Rajasthan":"Rajasthan",
                            "MP Nagar Madhya Pradesh":"Madhya Pradesh",
                            "Antop Hill Maharashtra":"Maharashtra",
                            "Avenue_DPC West Bengal":"West Bengal",
                            "Nagar Uttar Pradesh":"Uttar Pradesh",
                            "Balaji Nagar Maharashtra":"Maharashtra",
                            "Kothanur_L Karnataka":"Karnataka",
                            "Rahatani DPC Maharashtra":"Maharashtra",
                            "Mahim Maharashtra":"Maharashtra",
                            "DC Maharashtra":"Maharashtra",
                            "_NAD Andhra Pradesh":"Andhra Pradesh",
                           "Delhi Delhi":"Delhi",
                           "West_Dc Maharashtra":"Maharashtra",
                           "Hub Maharashtra":"Maharashtra"
                                                       })


# ================================================================================
# CODE CELL 55
# ================================================================================

df["destination_city"].replace({
    "del":"Delhi"
},inplace=True)
df["source_city"].replace({
    "del":"Delhi"
},inplace=True)


# ================================================================================
# MARKDOWN CELL 56
# ================================================================================
# 
# 


# ================================================================================
# CODE CELL 57
# ================================================================================

df["source_city"].replace({
    "Bangalore":"Bengaluru"
        },inplace=True)
df["destination_city"].replace({
    "Bangalore":"Bengaluru"
        },inplace=True)
df["destination_city"].replace({
    "AMD":"Ahmedabad"
        },inplace=True)
df["destination_city"].replace({
    "Amdavad":"Ahmedabad"
        },inplace=True)
df["source_city"].replace({
    "AMD":"Ahmedabad"
        },inplace=True)
df["source_city"].replace({
    "Amdavad":"Ahmedabad"
        },inplace=True)


# ================================================================================
# CODE CELL 58
# ================================================================================

df["source_city_state"] = df["source_city"] + " " + df["source_state"]
df["destination_city_state"] = df["destination_city"] + " " + df["destination_state"]


# ================================================================================
# CODE CELL 59
# ================================================================================

df["source_city_state"].nunique()


# ================================================================================
# CODE CELL 60
# ================================================================================

df["destination_city_state"].nunique()


# ================================================================================
# CODE CELL 61
# ================================================================================

df["source_state"].nunique()


# ================================================================================
# CODE CELL 62
# ================================================================================

df["destination_state"].nunique()


# ================================================================================
# CODE CELL 63
# ================================================================================

## Delhivery delivered in approdimately 1250 cities and almost all the states all over in india. 


# ================================================================================
# CODE CELL 64
# ================================================================================

data = df.copy()


# ================================================================================
# CODE CELL 65
# ================================================================================

data.columns


# ================================================================================
# CODE CELL 66
# ================================================================================

# data[["source_city","source_state","destination_city","destination_state","source_city_state","destination_city_state"]].fillna()


# ================================================================================
# CODE CELL 67
# ================================================================================

# above data we impute after aggregating as per tripIDs. 


# ================================================================================
# CODE CELL 68
# ================================================================================

data.columns


# ================================================================================
# CODE CELL 69
# ================================================================================

data.drop(['source_center',"source_name","destination_center","destination_name","cutoff_timestamp"],axis = 1,inplace=True)


# ================================================================================
# CODE CELL 70
# ================================================================================

data.drop(["od_end_time","od_start_time"],axis = 1 , inplace=True)


# ================================================================================
# CODE CELL 71
# ================================================================================

data


# ================================================================================
# MARKDOWN CELL 72
# ================================================================================
# # Aggregating Data : 


# ================================================================================
# CODE CELL 73
# ================================================================================

actual_time = data.groupby(["trip_uuid",
              "start_scan_to_end_scan"])["actual_time"].max().reset_index().groupby("trip_uuid")["actual_time"].sum().reset_index()
segment_osrm_time = data[["trip_uuid","segment_osrm_time"]].groupby("trip_uuid")["segment_osrm_time"].sum().reset_index()
segment_actual_time = data.groupby("trip_uuid")["segment_actual_time"].sum().reset_index()
osrm_time = data.groupby(["trip_uuid",
              "start_scan_to_end_scan"])["osrm_time"].max().reset_index().groupby("trip_uuid")["osrm_time"].sum().reset_index()
time_taken_btwn_odstart_and_od_end = data.groupby("trip_uuid")["time_taken_btwn_odstart_and_od_end"].unique().reset_index()

time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"] = time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"].apply(sum)
start_scan_to_end_scan = ((data.groupby("trip_uuid")["start_scan_to_end_scan"].unique())).reset_index()
start_scan_to_end_scan["start_scan_to_end_scan"] = start_scan_to_end_scan["start_scan_to_end_scan"].apply(sum) 

osrm_distance = data.groupby(["trip_uuid",
              "start_scan_to_end_scan"])["osrm_distance"].max().reset_index().groupby("trip_uuid")["osrm_distance"].sum().reset_index()
actual_distance_to_destination = data.groupby(["trip_uuid",
              "start_scan_to_end_scan"])["actual_distance_to_destination"].max().reset_index().groupby("trip_uuid")["actual_distance_to_destination"].sum().reset_index()
segment_osrm_distance = data[["trip_uuid",
                              "segment_osrm_distance"]].groupby("trip_uuid")["segment_osrm_distance"].sum().reset_index()


# ================================================================================
# MARKDOWN CELL 74
# ================================================================================
# ****


# ================================================================================
# MARKDOWN CELL 75
# ================================================================================
# # Hypothesis Tests for time durations and distance related features : 
# 


# ================================================================================
# MARKDOWN CELL 76
# ================================================================================
# ****


# ================================================================================
# MARKDOWN CELL 77
# ================================================================================
# ## Analysing TimeTaken Between OdStart and OdEnd time & StartScanToEndScan : 


# ================================================================================
# MARKDOWN CELL 78
# ================================================================================
# > #### H0: Mean of time taken betweenn trip end ans start time = Mean of start and end scan time
# > #### Ha: Mean of time taken betweenn trip end ans start time != Mean of start and end scan time
# 


# ================================================================================
# CODE CELL 79
# ================================================================================

plt.figure(figsize=(15,5))
plt.subplot(121)
sns.distplot((time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"]))
plt.subplot(122)
sns.distplot((start_scan_to_end_scan["start_scan_to_end_scan"]))


# ================================================================================
# CODE CELL 80
# ================================================================================

# KS-test : checking the distributions how closly equal thy are : 


# ================================================================================
# CODE CELL 81
# ================================================================================

stats.ks_2samp(time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"]
               ,start_scan_to_end_scan["start_scan_to_end_scan"])


# ================================================================================
# CODE CELL 82
# ================================================================================

for i in range(5):
    print(stats.ttest_ind((time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"].sample(3000))
                ,(start_scan_to_end_scan["start_scan_to_end_scan"].sample(3000))))


# ================================================================================
# MARKDOWN CELL 83
# ================================================================================
# > #### from Kolmogorov–Smirnov test , p-value is 0.9943 , from which we can conclude  tht both the distributions
# 
# > #### (time_taken_btwn_odstart_and_od_end and start_scan_to_end_scan) are closly similar.
# 
# 
# > ####  from 2 sample t-test ,we can also conclude that Average time_taken_btwn_odstart_and_od_end for population is also equal to Average start_scan_to_end_scan for population.


# ================================================================================
# CODE CELL 84
# ================================================================================

# also checking mean and standard deviation for timetaken and scan times : 


# ================================================================================
# CODE CELL 85
# ================================================================================

time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"].mean(),time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"].std()


# ================================================================================
# CODE CELL 86
# ================================================================================

start_scan_to_end_scan["start_scan_to_end_scan"].mean(),start_scan_to_end_scan["start_scan_to_end_scan"].std()


# ================================================================================
# CODE CELL 87
# ================================================================================

# variance and means both are closly similar for scan time and trip start and end time taken 


# ================================================================================
# CODE CELL 88
# ================================================================================




# ================================================================================
# MARKDOWN CELL 89
# ================================================================================
# ## Analysing Actual Time taken to complete the delivery  &  start-scan-end-scan


# ================================================================================
# MARKDOWN CELL 90
# ================================================================================
# > #### H0: Mean of start and end scan time <=  Mean of Actual time taken to complete delivery 
# > #### Ha: Mean of start and end scan time  > Mean of Actual time taken to complete delivery
# 


# ================================================================================
# CODE CELL 91
# ================================================================================

plt.figure(figsize=(15,5))
plt.subplot(121)
sns.distplot((actual_time["actual_time"]))
plt.subplot(122)
sns.distplot((start_scan_to_end_scan["start_scan_to_end_scan"]))


# ================================================================================
# CODE CELL 92
# ================================================================================

stats.ks_2samp(actual_time["actual_time"],start_scan_to_end_scan["start_scan_to_end_scan"])


# ================================================================================
# CODE CELL 93
# ================================================================================

for i in range(7):
    print(stats.ttest_ind((actual_time["actual_time"].sample(3000))
                ,(start_scan_to_end_scan["start_scan_to_end_scan"].sample(3000)),alternative="less"))


# ================================================================================
# MARKDOWN CELL 94
# ================================================================================
# > #### from KS test for actual-time and start_scan_to_end_scan distributions are not same.
# 
# > #### from ttest of population average actual_time is less than population average start_scan_to_end_scan.


# ================================================================================
# CODE CELL 95
# ================================================================================

actual_time["actual_time"].mean(),actual_time["actual_time"].std()


# ================================================================================
# CODE CELL 96
# ================================================================================

start_scan_to_end_scan["start_scan_to_end_scan"].mean(),start_scan_to_end_scan["start_scan_to_end_scan"].std()


# ================================================================================
# CODE CELL 97
# ================================================================================




# ================================================================================
# MARKDOWN CELL 98
# ================================================================================
# ## Analysing Actual Time & TimeTaken between start and end trip time. 


# ================================================================================
# MARKDOWN CELL 99
# ================================================================================
# > #### H0: Mean of Actual time taken to complete delivery =  Mean of time taken betweenn trip end and start time
# > #### Ha: Mean of Actual time taken to complete delivery  !=  Mean of time taken betweenn trip end and start time


# ================================================================================
# CODE CELL 100
# ================================================================================

stats.ks_2samp(actual_time["actual_time"],time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"])


# ================================================================================
# CODE CELL 101
# ================================================================================

for i in range(5):
    print(stats.ttest_ind((actual_time["actual_time"].sample(1000))
                ,(time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"].sample(1000))))


# ================================================================================
# MARKDOWN CELL 102
# ================================================================================
# > #### from above kstest of distribution and two sample ttest , 
# > #### we can conclude that population mean Actual time taken to complete delivery and population mean time_taken_btwn_od_start_and_od_end are also not same.


# ================================================================================
# CODE CELL 103
# ================================================================================




# ================================================================================
# MARKDOWN CELL 104
# ================================================================================
# ## Analysing  Actual Time   taken to complete delivery from source to destination hub    &   OSRM measured time : 


# ================================================================================
# MARKDOWN CELL 105
# ================================================================================
# > #### H0: Mean of OSRM time  >=  Mean of Actual time taken to complete delivery
# > #### Ha: Mean of OSRM time  <  Mean of Actual time taken to complete delivery 


# ================================================================================
# CODE CELL 106
# ================================================================================

plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((actual_time["actual_time"])))
plt.subplot(122)
sns.distplot(((osrm_time["osrm_time"])))


# ================================================================================
# CODE CELL 107
# ================================================================================

stats.ks_2samp(actual_time["actual_time"],
               osrm_time["osrm_time"])


# ================================================================================
# CODE CELL 108
# ================================================================================

for i in range(5):
    print(stats.ttest_ind(actual_time["actual_time"].sample(5000),
               osrm_time["osrm_time"].sample(5000),alternative='greater'))


# ================================================================================
# MARKDOWN CELL 109
# ================================================================================
# > #### from two sample ttest can conclude , that population mean actual time taken to complete delivert from source to warehouse and orsm estimate mean time for population are not same. 
# > #### actual time is higher than the osrm estimated time for delivery.


# ================================================================================
# CODE CELL 110
# ================================================================================

actual_time["actual_time"].mean(),actual_time["actual_time"].std()


# ================================================================================
# CODE CELL 111
# ================================================================================

osrm_time["osrm_time"].mean(),osrm_time["osrm_time"].std()


# ================================================================================
# CODE CELL 112
# ================================================================================




# ================================================================================
# MARKDOWN CELL 113
# ================================================================================
# ## Analysing Actual Time taken to complete delivery from source to destination hub & Segment Actual Time :  


# ================================================================================
# MARKDOWN CELL 114
# ================================================================================
# > #### H0: Actual time = segment actual time
# > #### Ha: Actual time != segment actual time


# ================================================================================
# CODE CELL 115
# ================================================================================

plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((actual_time["actual_time"])))
plt.subplot(122)
sns.distplot(((segment_actual_time["segment_actual_time"])))


# ================================================================================
# CODE CELL 116
# ================================================================================

for i in range(7):
    print(stats.ttest_ind((actual_time["actual_time"].sample(3000)),
                (segment_actual_time["segment_actual_time"].sample(3000))))


# ================================================================================
# MARKDOWN CELL 117
# ================================================================================
# > #### from two sample ttest , we can conclude that
# > #### Population average for
# > #### Actual Time taken to complete delivery trip and segment actual time are same. 
# 


# ================================================================================
# CODE CELL 118
# ================================================================================

actual_time["actual_time"].mean(),actual_time["actual_time"].std()


# ================================================================================
# CODE CELL 119
# ================================================================================

segment_actual_time["segment_actual_time"].mean(),segment_actual_time["segment_actual_time"].std()


# ================================================================================
# CODE CELL 120
# ================================================================================




# ================================================================================
# MARKDOWN CELL 121
# ================================================================================
# ## Analysing osrm Time  & segment-osrm-time :  


# ================================================================================
# MARKDOWN CELL 122
# ================================================================================
# > #### H0: segment actual time <= OSRM time
# > #### Ha: segment actual time > OSRM time


# ================================================================================
# CODE CELL 123
# ================================================================================

plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((osrm_time["osrm_time"])))
plt.subplot(122)
sns.distplot(((segment_osrm_time["segment_osrm_time"])))


# ================================================================================
# CODE CELL 124
# ================================================================================

for i in range(7):
    print(stats.ttest_ind((osrm_time["osrm_time"].sample(3000)),
                (segment_osrm_time["segment_osrm_time"].sample(3000)),alternative ="less"))


# ================================================================================
# MARKDOWN CELL 125
# ================================================================================
# > #### from ttest , we can conclude that 
# > #### average of osrm Time & segment-osrm-time for population is not same. 
# > #### Population Mean osrm time  is less than Population Mean segment osrm time.
# 


# ================================================================================
# CODE CELL 126
# ================================================================================

osrm_time["osrm_time"].mean(),osrm_time["osrm_time"].std()


# ================================================================================
# CODE CELL 127
# ================================================================================

segment_osrm_time["segment_osrm_time"].mean(),segment_osrm_time["segment_osrm_time"].std()


# ================================================================================
# CODE CELL 128
# ================================================================================




# ================================================================================
# MARKDOWN CELL 129
# ================================================================================
# # Analysing Distances measures : 


# ================================================================================
# MARKDOWN CELL 130
# ================================================================================
# ## Analysing and Visulizing OSRM Estimated distance and Segment-osrm-distance  :


# ================================================================================
# MARKDOWN CELL 131
# ================================================================================
# > #### H0 : Segment OSRM distnace <= OSRM distnace
# > #### Ha : Segment OSRM distnace > OSRM distnace


# ================================================================================
# CODE CELL 132
# ================================================================================

plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((osrm_distance["osrm_distance"])))
plt.subplot(122)
sns.distplot(((segment_osrm_distance["segment_osrm_distance"])))


# ================================================================================
# CODE CELL 133
# ================================================================================

stats.ks_2samp(osrm_distance["osrm_distance"],segment_osrm_distance["segment_osrm_distance"])


# ================================================================================
# CODE CELL 134
# ================================================================================

for i in range(7):
    print(stats.ttest_ind(osrm_distance["osrm_distance"].sample(5000),
               segment_osrm_distance["segment_osrm_distance"].sample(5000),alternative="less"))


# ================================================================================
# MARKDOWN CELL 135
# ================================================================================
# 


# ================================================================================
# CODE CELL 136
# ================================================================================

osrm_distance["osrm_distance"].mean(),osrm_distance["osrm_distance"].std()


# ================================================================================
# CODE CELL 137
# ================================================================================

segment_osrm_distance["segment_osrm_distance"].mean(),segment_osrm_distance["segment_osrm_distance"].std()


# ================================================================================
# MARKDOWN CELL 138
# ================================================================================
# >    #### from KS test , we can conclude the distributions of segment osrm distance and osrm distnace are not same! 
# >    #### from two sample one sided ttest, we can conclude: Average of osrm distance for population is less than  average of segment osrm distnace 


# ================================================================================
# CODE CELL 139
# ================================================================================




# ================================================================================
# CODE CELL 140
# ================================================================================




# ================================================================================
# CODE CELL 141
# ================================================================================




# ================================================================================
# CODE CELL 142
# ================================================================================




# ================================================================================
# MARKDOWN CELL 143
# ================================================================================
# ## Analysing and Visulizing OSRM Estimated distance and Actual Distance between source and destination warehouse :


# ================================================================================
# MARKDOWN CELL 144
# ================================================================================
# > #### H0 : Mean OSRM distance <= Mean Actual distnace 
# > #### Ha : Mean OSRM distance > Mean Actual distnace 


# ================================================================================
# CODE CELL 145
# ================================================================================

plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((osrm_distance["osrm_distance"])))
plt.subplot(122)
sns.distplot(((actual_distance_to_destination["actual_distance_to_destination"])))


# ================================================================================
# CODE CELL 146
# ================================================================================

stats.ks_2samp(osrm_distance["osrm_distance"],actual_distance_to_destination["actual_distance_to_destination"])


# ================================================================================
# CODE CELL 147
# ================================================================================

for i in range(5):
    print(stats.ttest_ind(osrm_distance["osrm_distance"].sample(5000),
               actual_distance_to_destination["actual_distance_to_destination"].sample(5000),alternative="greater"))


# ================================================================================
# MARKDOWN CELL 148
# ================================================================================
# > #### From left sided ttest , we can conclude 
# > #### for population OSRM estimated distance is higher than the actual distance  from source to destination warehouse. 


# ================================================================================
# CODE CELL 149
# ================================================================================

osrm_distance["osrm_distance"].mean(),osrm_distance["osrm_distance"].std()


# ================================================================================
# CODE CELL 150
# ================================================================================

actual_distance_to_destination["actual_distance_to_destination"].mean(),actual_distance_to_destination["actual_distance_to_destination"].std()


# ================================================================================
# MARKDOWN CELL 151
# ================================================================================
# ****


# ================================================================================
# MARKDOWN CELL 152
# ================================================================================
# ****
# ****


# ================================================================================
# CODE CELL 153
# ================================================================================




# ================================================================================
# CODE CELL 154
# ================================================================================




# ================================================================================
# CODE CELL 155
# ================================================================================




# ================================================================================
# MARKDOWN CELL 156
# ================================================================================
# ****


# ================================================================================
# MARKDOWN CELL 157
# ================================================================================
# # Merging All the numerical Fields as per TripID: 


# ================================================================================
# CODE CELL 160
# ================================================================================




# ================================================================================
# CODE CELL 161
# ================================================================================

distances = segment_osrm_distance.merge(actual_distance_to_destination.merge(osrm_distance,
                                                                             on="trip_uuid"),
                                                                            on="trip_uuid")


# ================================================================================
# CODE CELL 162
# ================================================================================

time = segment_osrm_time.merge(osrm_time.merge(segment_actual_time.merge(actual_time.merge(time_taken_btwn_odstart_and_od_end.merge(start_scan_to_end_scan,
                                         on="trip_uuid",
                                         ),on="trip_uuid"),on="trip_uuid"),on="trip_uuid"),on="trip_uuid")


# ================================================================================
# CODE CELL 163
# ================================================================================

Merge1 = time.merge(distances,on="trip_uuid",
                                        )


# ================================================================================
# CODE CELL 164
# ================================================================================




# ================================================================================
# CODE CELL 165
# ================================================================================

Merge1


# ================================================================================
# CODE CELL 166
# ================================================================================




# ================================================================================
# CODE CELL 167
# ================================================================================




# ================================================================================
# CODE CELL 168
# ================================================================================




# ================================================================================
# CODE CELL 169
# ================================================================================




# ================================================================================
# CODE CELL 170
# ================================================================================




# ================================================================================
# CODE CELL 171
# ================================================================================




# ================================================================================
# CODE CELL 172
# ================================================================================




# ================================================================================
# CODE CELL 173
# ================================================================================




# ================================================================================
# MARKDOWN CELL 174
# ================================================================================
# #  Merging Location details and route_type and Numerical data on TripID : 


# ================================================================================
# CODE CELL 175
# ================================================================================

city = data.groupby("trip_uuid")[["source_city",
                                  "destination_city"]].aggregate({
        "source_city":pd.unique,
    "destination_city":pd.unique,
})

state = data.groupby("trip_uuid")[["source_state",
                                   "destination_state"]].aggregate({
        "source_state":pd.unique,
    "destination_state":pd.unique,
})

city_state = data.groupby("trip_uuid")[["source_city_state",
                                        "destination_city_state"]].aggregate({
        "source_city_state":pd.unique,
    "destination_city_state":pd.unique,
})

locations = city.merge(city_state.merge(state,on="trip_uuid"
                            ,how="outer"),
           on="trip_uuid",
           how="outer")


# ================================================================================
# CODE CELL 176
# ================================================================================




# ================================================================================
# CODE CELL 177
# ================================================================================

route_type = data.groupby("trip_uuid")["route_type"].unique().reset_index()


# ================================================================================
# CODE CELL 178
# ================================================================================

Merged = route_type.merge(locations.merge(Merge1,on="trip_uuid",
           how="outer"),
                 on="trip_uuid",
           how="outer"
                )


# ================================================================================
# CODE CELL 179
# ================================================================================

trip_records = Merged.copy()


# ================================================================================
# CODE CELL 180
# ================================================================================

trip_records["route_type"] = trip_records["route_type"].apply(lambda x:x[0])


# ================================================================================
# CODE CELL 181
# ================================================================================

route_to_merge = data.groupby("trip_uuid")["route_schedule_uuid"].unique().reset_index()


# ================================================================================
# CODE CELL 182
# ================================================================================

trip_records = trip_records.merge(route_to_merge,on="trip_uuid",how="outer")


# ================================================================================
# CODE CELL 183
# ================================================================================

trip_records["route_schedule_uuid"] = trip_records["route_schedule_uuid"].apply(lambda x:x[0])


# ================================================================================
# CODE CELL 184
# ================================================================================

trip_records


# ================================================================================
# CODE CELL 185
# ================================================================================




# ================================================================================
# CODE CELL 186
# ================================================================================




# ================================================================================
# CODE CELL 187
# ================================================================================

# route_df['source'] = route_df['source'].str.strip("{''}")


# ================================================================================
# CODE CELL 188
# ================================================================================

trip_records.isna().sum()


# ================================================================================
# CODE CELL 189
# ================================================================================




# ================================================================================
# CODE CELL 190
# ================================================================================

trip_records.loc[trip_records.isnull().any(axis=1)]


# ================================================================================
# CODE CELL 191
# ================================================================================

trip_records[trip_records["trip_uuid"]=="trip-153852612674280168"]


# ================================================================================
# CODE CELL 192
# ================================================================================

trip_records.dropna(axis= 0,how = 'any',inplace = True)


# ================================================================================
# CODE CELL 193
# ================================================================================




# ================================================================================
# CODE CELL 194
# ================================================================================

trip_records["source_city"] = trip_records["source_city"].astype("str").str.strip("[]").str.replace("'","")
trip_records["destination_city"] = trip_records["destination_city"].astype("str").str.strip("[]").str.replace("'","")
trip_records["source_city_state"] = trip_records["source_city_state"].astype("str").str.strip("[]").str.replace("'","")
trip_records["destination_city_state"] = trip_records["destination_city_state"].astype("str").str.strip("[]").str.replace("'","")

trip_records["source_state"] = trip_records["source_state"].astype("str").str.strip("[]").str.replace("'","")
trip_records["destination_state"] = trip_records["destination_state"].astype("str").str.strip("[]").str.replace("'","")


# ================================================================================
# CODE CELL 195
# ================================================================================




# ================================================================================
# CODE CELL 196
# ================================================================================




# ================================================================================
# MARKDOWN CELL 197
# ================================================================================
# ### Checking if any null values left in Trip Records Data : 


# ================================================================================
# CODE CELL 198
# ================================================================================

trip_records.isna().sum()


# ================================================================================
# CODE CELL 199
# ================================================================================




# ================================================================================
# CODE CELL 200
# ================================================================================




# ================================================================================
# CODE CELL 201
# ================================================================================

trip_records.loc[trip_records.isnull().any(axis=1)]


# ================================================================================
# CODE CELL 202
# ================================================================================

trip_records.corr()


# ================================================================================
# CODE CELL 203
# ================================================================================

trip_records.to_csv("trip_records.csv")


# ================================================================================
# MARKDOWN CELL 204
# ================================================================================
# ## Treating Outliers : 


# ================================================================================
# CODE CELL 205
# ================================================================================

plt.figure(figsize = (10,8))
plt.subplot(121)
trip_records[['segment_osrm_time', 'osrm_time',
       'segment_actual_time', 'actual_time',
       'time_taken_btwn_odstart_and_od_end', 'start_scan_to_end_scan']].boxplot()
plt.xticks(rotation =90)
plt.subplot(122)
trip_records[['segment_osrm_distance', 'actual_distance_to_destination',
       'osrm_distance']].boxplot()
plt.xticks(rotation =90)
plt.show()


# ================================================================================
# CODE CELL 206
# ================================================================================

outlier_treatment  = trip_records.copy()


# ================================================================================
# CODE CELL 207
# ================================================================================

outlier_treatment_num = outlier_treatment[['segment_osrm_time', 'osrm_time',
       'segment_actual_time', 'actual_time',
       'time_taken_btwn_odstart_and_od_end', 'start_scan_to_end_scan',
        'segment_osrm_distance', 'actual_distance_to_destination',
        'osrm_distance']]


# ================================================================================
# CODE CELL 208
# ================================================================================




# ================================================================================
# CODE CELL 209
# ================================================================================

# outlier_treatment_num[(np.abs(stats.zscore(outlier_treatment_num)) < 3).all(axis=1)]


# ================================================================================
# MARKDOWN CELL 210
# ================================================================================
# ## After removing outliers from all numerical features :  


# ================================================================================
# CODE CELL 211
# ================================================================================

trip_records_without_outliers = trip_records.loc[outlier_treatment_num[(np.abs(stats.zscore(outlier_treatment_num)) < 3).all(axis=1)].index]
trip_records_without_outliers


# ================================================================================
# CODE CELL 212
# ================================================================================

trip_records_without_outliers = trip_records_without_outliers[['trip_uuid','route_type','source_city_state', 'destination_city_state','segment_osrm_time', 'osrm_time',
       'segment_actual_time', 'actual_time',
       'time_taken_btwn_odstart_and_od_end', 'start_scan_to_end_scan',
       'segment_osrm_distance', 'actual_distance_to_destination',
       'osrm_distance']]


# ================================================================================
# CODE CELL 213
# ================================================================================

plt.figure(figsize = (10,8))
plt.subplot(121)
trip_records_without_outliers[['segment_osrm_time', 'osrm_time',
       'segment_actual_time', 'actual_time',
       'time_taken_btwn_odstart_and_od_end', 'start_scan_to_end_scan']].boxplot()
plt.xticks(rotation =90)
plt.subplot(122)
trip_records_without_outliers[['segment_osrm_distance', 'actual_distance_to_destination',
       'osrm_distance']].boxplot()
plt.xticks(rotation =90)
plt.show()


# ================================================================================
# CODE CELL 214
# ================================================================================




# ================================================================================
# MARKDOWN CELL 215
# ================================================================================
# ## Processing Data for One hot encoding : 
# 
# ### merging locations details into one columns . and re categorise the data as per highest trips having location as top category 
# 


# ================================================================================
# CODE CELL 216
# ================================================================================

trip_records_without_outliers["destination_source_locations"] = trip_records_without_outliers["source_city_state"]+" "+trip_records_without_outliers["destination_city_state"]
trip_records_without_outliers.drop(["source_city_state","destination_city_state"],axis = 1,inplace=True)


# ================================================================================
# CODE CELL 217
# ================================================================================

sc_dc = trip_records_without_outliers.groupby(["destination_source_locations"])["trip_uuid"].nunique().sort_values(ascending= False).reset_index()


# ================================================================================
# CODE CELL 218
# ================================================================================

# trip_records.groupby(['source_state','destination_state'])["trip_uuid"].nunique().sort_values(ascending= False).reset_index().head(30)


# ================================================================================
# CODE CELL 219
# ================================================================================

def get_cat(H):
    if 0 <= H <= 50:
        return "Category 7"
    elif 51 <= H <= 100:
        return "Category 6"
    elif 101 <= H <= 200:
        return "Category 5"
    elif 201 <= H <= 300:
        return "Category 4"
    elif 301 <= H <= 400:
        return "Category 3"
    elif 401 <= H <= 500:
        return "Category 2"
    else:
        return "Category 1"


# ================================================================================
# CODE CELL 220
# ================================================================================

sc_dc["city"]  = pd.Series(map(get_cat,sc_dc["trip_uuid"]))


# ================================================================================
# CODE CELL 221
# ================================================================================

trip_records_for_encoding = sc_dc.merge(trip_records_without_outliers,
            on="destination_source_locations")
trip_records_for_encoding.drop(["destination_source_locations","trip_uuid_x"],axis = 1,inplace=True)


# ================================================================================
# CODE CELL 222
# ================================================================================

trip_records_for_encoding.drop(["trip_uuid_y"],axis = 1,inplace=True)
# trip_records_for_encoding.sample(15)


# ================================================================================
# CODE CELL 223
# ================================================================================

encoded_data = pd.get_dummies(trip_records_for_encoding,
             columns=["route_type","city"] )


# ================================================================================
# CODE CELL 224
# ================================================================================

encoded_data


# ================================================================================
# CODE CELL 225
# ================================================================================

['segment_osrm_time', 'osrm_time',
       'segment_actual_time', 'actual_time',
       'time_taken_btwn_odstart_and_od_end', 'start_scan_to_end_scan' ,'segment_osrm_distance', 'actual_distance_to_destination','osrm_distance' ]


# ================================================================================
# CODE CELL 226
# ================================================================================

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler


# ================================================================================
# CODE CELL 227
# ================================================================================

scaler = StandardScaler()
std_data = scaler.fit_transform(encoded_data[['segment_osrm_time',
 'osrm_time',
 'segment_actual_time',
 'actual_time',
 'time_taken_btwn_odstart_and_od_end',
 'start_scan_to_end_scan',
 'segment_osrm_distance',
 'actual_distance_to_destination',
 'osrm_distance']])
std_data = pd.DataFrame(std_data, columns=['segment_osrm_time',
 'osrm_time',
 'segment_actual_time',
 'actual_time',
 'time_taken_btwn_odstart_and_od_end',
 'start_scan_to_end_scan',
 'segment_osrm_distance',
 'actual_distance_to_destination',
 'osrm_distance'])
std_data.head()


# ================================================================================
# CODE CELL 228
# ================================================================================




# ================================================================================
# CODE CELL 229
# ================================================================================

scaler = MinMaxScaler()
MinMax_data = scaler.fit_transform(encoded_data[['segment_osrm_time','osrm_time','segment_actual_time','actual_time',
 'time_taken_btwn_odstart_and_od_end','start_scan_to_end_scan','segment_osrm_distance','actual_distance_to_destination',
 'osrm_distance']])
MinMax_data = pd.DataFrame(MinMax_data,columns=['segment_osrm_time',
 'osrm_time','segment_actual_time','actual_time','time_taken_btwn_odstart_and_od_end','start_scan_to_end_scan',
 'segment_osrm_distance','actual_distance_to_destination','osrm_distance'])
MinMax_data.head()


# ================================================================================
# CODE CELL 230
# ================================================================================

std_data


# ================================================================================
# CODE CELL 231
# ================================================================================




# ================================================================================
# CODE CELL 232
# ================================================================================

one_hot_encoded_data = encoded_data[["route_type_Carting","route_type_FTL","city_Category 1",
 "city_Category 2","city_Category 3","city_Category 4",
 "city_Category 5","city_Category 6","city_Category 7"]]


# ================================================================================
# CODE CELL 233
# ================================================================================

Standardized_Data = pd.concat([std_data,one_hot_encoded_data],axis = 1)


# ================================================================================
# CODE CELL 234
# ================================================================================

Min_Max_Scaled_Data = pd.concat([MinMax_data,one_hot_encoded_data],axis = 1)


# ================================================================================
# CODE CELL 235
# ================================================================================

Standardized_Data.sample(5)


# ================================================================================
# CODE CELL 236
# ================================================================================

Min_Max_Scaled_Data.sample(5)


# ================================================================================
# CODE CELL 237
# ================================================================================




# ================================================================================
# MARKDOWN CELL 238
# ================================================================================
# # Route analysis : 


# ================================================================================
# CODE CELL 239
# ================================================================================

A = data.groupby("route_schedule_uuid")["route_type"].unique().reset_index()
B = data.groupby("route_schedule_uuid")["destination_city"].unique().reset_index()
B.columns = ["route_schedule_uuid","destination_cities"]
C = data.groupby("route_schedule_uuid")["source_city"].unique().reset_index()
C.columns = ["route_schedule_uuid","source_cities"]
D = data.groupby("route_schedule_uuid")["source_state"].unique().reset_index()
D.columns = ["route_schedule_uuid","source_states"]
E = data.groupby("route_schedule_uuid")["destination_state"].unique().reset_index()
E.columns = ["route_schedule_uuid","destination_states"]
F = data.groupby("route_schedule_uuid")[["source_state",
                                         "destination_state"]].nunique().sort_values(by="source_state",
                                                                                     ascending=False).reset_index()
F.columns = ["route_schedule_uuid","#source_states"
             ,"#destination_states"]
G = trip_records.groupby("route_schedule_uuid")["actual_distance_to_destination"].mean().reset_index()
G.columns = ["route_schedule_uuid","Average_Actual_distance_to_destination"]
H = trip_records["route_schedule_uuid"].value_counts().reset_index()
H.columns = ["route_schedule_uuid","Number_of_Trips"]


# ================================================================================
# CODE CELL 240
# ================================================================================

I = data.groupby("route_schedule_uuid")[["source_city",
                                         "destination_city"]].nunique().sort_values(by="source_city",
                                                                                     ascending=False).reset_index()
I.columns = ["route_schedule_uuid","#source_cities"
             ,"#destination_cities"]


# ================================================================================
# CODE CELL 241
# ================================================================================

route_records = I.merge(H.merge(G.merge(F.merge(E.merge(D.merge(C.merge(A.merge(B,
        on ="route_schedule_uuid",
        how = "outer"),on ="route_schedule_uuid",
        how = "outer"),
       on ="route_schedule_uuid",
        how = "outer"),
       on ="route_schedule_uuid",
        how = "outer"),
       on ="route_schedule_uuid",
        how = "outer"),
       on ="route_schedule_uuid",
        how = "outer"),
       on ="route_schedule_uuid",
        how = "outer"),on ="route_schedule_uuid",
        how = "outer")


# ================================================================================
# CODE CELL 242
# ================================================================================

# route_records.sort_values(by="Average_Actual_distance_to_destination",ascending=False)


# ================================================================================
# CODE CELL 243
# ================================================================================

route_records.isna().sum()


# ================================================================================
# CODE CELL 244
# ================================================================================

route_records.dropna(inplace=True)


# ================================================================================
# CODE CELL 245
# ================================================================================

route_records["route_type"] = route_records["route_type"].astype("str").str.strip("[]").str.replace("'","")
route_records["source_cities"] = route_records["source_cities"].astype("str").str.strip("[]").str.replace("'","")
route_records["destination_cities"] = route_records["destination_cities"].astype("str").str.strip("[]").str.replace("'","")
route_records["source_states"] = route_records["source_states"].astype("str").str.strip("[]").str.replace("'","")
                             
route_records["destination_states"] = route_records["destination_states"].astype("str").str.strip("[]").str.replace("'","")                        


# ================================================================================
# CODE CELL 246
# ================================================================================

route_records


# ================================================================================
# CODE CELL 247
# ================================================================================

route_records["ROUTE"] = route_records["source_cities"] + " -- " + route_records["destination_cities"]


# ================================================================================
# CODE CELL 248
# ================================================================================

route_records.drop(["route_schedule_uuid"],axis = 1,inplace=True)


# ================================================================================
# CODE CELL 249
# ================================================================================

first_column = route_records.pop('ROUTE')
route_records.insert(0, 'ROUTE', first_column) 


# ================================================================================
# CODE CELL 250
# ================================================================================

route_records["SouceToDestination_city"] = route_records["source_cities"].str.split(" ").apply(lambda x:x[0]) +" TO " +route_records["destination_cities"].str.split(" ").apply(lambda x:x[-1])


# ================================================================================
# CODE CELL 251
# ================================================================================

first_column = route_records.pop('SouceToDestination_city')
route_records.insert(0, 'SouceToDestination_city', first_column) 


# ================================================================================
# CODE CELL 252
# ================================================================================

route_records


# ================================================================================
# CODE CELL 253
# ================================================================================

route_records.to_csv("route_records.csv")


# ================================================================================
# CODE CELL 254
# ================================================================================




# ================================================================================
# CODE CELL 255
# ================================================================================




# ================================================================================
# CODE CELL 256
# ================================================================================




# ================================================================================
# MARKDOWN CELL 257
# ================================================================================
# ##  Exploratory Data Analysis : ( getting some  insights from preprocessed data ) : 


# ================================================================================
# CODE CELL 258
# ================================================================================




# ================================================================================
# CODE CELL 259
# ================================================================================




# ================================================================================
# MARKDOWN CELL 260
# ================================================================================
# ## Busiest Route Analysis : 
# 


# ================================================================================
# MARKDOWN CELL 261
# ================================================================================
# ### Number of Trips between cities , sorted highest to lowest
# > #### Top 20 source and destination cities wihc have high freqency of trips in between . 


# ================================================================================
# CODE CELL 262
# ================================================================================

Number_of_trips_between_cities = data.groupby(["source_city_state",
                                               "destination_city_state"])["trip_uuid"].nunique().sort_values(ascending=False).reset_index()
Number_of_trips_between_cities.head(25)


# ================================================================================
# MARKDOWN CELL 263
# ================================================================================
# > ##### From above table, we can observe that Mumbai Maharashtra ,Delhi ,Gurgaon(Haryana),Bengaluru Karnataka	,Hyderabad Telangana,Chennai Tamil Nadu,Ahmedabad Gujarat,Pune Maharashtra,Chandigarh Chandigarh and Kolkata West Bengal	 are some cities have higest amount of trips happening states with in the city :	


# ================================================================================
# CODE CELL 264
# ================================================================================

Number_of_trips_between_cities.loc[Number_of_trips_between_cities["source_city_state"] != Number_of_trips_between_cities["destination_city_state"]].head(25)


# ================================================================================
# MARKDOWN CELL 265
# ================================================================================
# > ##### If we talk about , not having equal source and destination states , source and destination cities having higest number of trips in between are : 
#         delhi to gurgao
#         Gurgaon,Haryana TO Bengaluru,Karnataka
#         Bhiwandi/Mumbai,Maharashtra TO Pune Maharashtra
#         Sonipat TO	Gurgaon,Haryana
#         
#       - it is also been observed that lots of deliveries are happening to airpots 
#       - like : Chennai to MAA chennai international Airport , Pune to Pune Airport (PNQ),Kolkata to	CCU West Bengal Kolkata International Airport , Bengluru to BLR-Bengaluru Internation Airport etc. 
#         


# ================================================================================
# CODE CELL 266
# ================================================================================




# ================================================================================
# CODE CELL 267
# ================================================================================




# ================================================================================
# CODE CELL 268
# ================================================================================

route_records[["ROUTE","Number_of_Trips",
               "Average_Actual_distance_to_destination",
               "#source_cities",
               "#destination_cities"]].sort_values(by="Number_of_Trips",ascending=False).head(25)


# ================================================================================
# MARKDOWN CELL 269
# ================================================================================
# #### Top Routes having Maximum Number of Trips between/within the source and destinations . 


# ================================================================================
# CODE CELL 270
# ================================================================================

plt.figure(figsize=(12,8))

X = route_records[["ROUTE", "Number_of_Trips",
               ]].sort_values(by="Number_of_Trips",ascending=False).head(35)
sns.barplot(y = X["ROUTE"],
           x= X["Number_of_Trips"])
plt.title("Number of trips per route")
plt.xticks(rotation = 90)
plt.show()


# ================================================================================
# CODE CELL 271
# ================================================================================

plt.figure(figsize=(12,8))

X = route_records[["ROUTE", "Average_Actual_distance_to_destination",
               ]].sort_values(by="Average_Actual_distance_to_destination",ascending=False).head(25)
sns.barplot(y = X["ROUTE"],
           x = X["Average_Actual_distance_to_destination"])
plt.xticks(rotation = 90)
plt.show()


# ================================================================================
# MARKDOWN CELL 272
# ================================================================================
# > #### From above Bar chart , and table , we can observe that higest trips are happening is with in the particular cities. 
# > #### in terms of average distnace between destinations , we can observe Guwahati to Mumbai , Benglore to Chandigarh ,Benglore to Delhi  , Benglore to Gurgaon are the longest routes .
# 


# ================================================================================
# CODE CELL 273
# ================================================================================




# ================================================================================
# CODE CELL 274
# ================================================================================




# ================================================================================
# CODE CELL 275
# ================================================================================




# ================================================================================
# CODE CELL 276
# ================================================================================

 


# ================================================================================
# CODE CELL 277
# ================================================================================




# ================================================================================
# CODE CELL 278
# ================================================================================




# ================================================================================
# MARKDOWN CELL 279
# ================================================================================
# # Busiest and Longest Routes : 


# ================================================================================
# CODE CELL 280
# ================================================================================




# ================================================================================
# CODE CELL 281
# ================================================================================

Busiest_and_Longest_Routes  = route_records[(route_records["Average_Actual_distance_to_destination"] > route_records["Average_Actual_distance_to_destination"].quantile(0.75)) 
              & (route_records["Number_of_Trips"] > route_records["Number_of_Trips"].quantile(0.75))].sort_values(by="Average_Actual_distance_to_destination"
                                                                                                                  ,ascending=False)


# ================================================================================
# CODE CELL 282
# ================================================================================

Busiest_and_Longest_Routes_top25 = Busiest_and_Longest_Routes[["source_cities",
                                                               "destination_cities",
                                                               "Number_of_Trips",
                                                               "Average_Actual_distance_to_destination"]].head(25)
Busiest_and_Longest_Routes_top25


# ================================================================================
# MARKDOWN CELL 283
# ================================================================================
# > #### Above Table shows the souce to destination city routes having largest numbers of trip happening having large distnaces :
#     which are : Chandigarh TO Bengaluru
#                 Gurgaon TO Bengaluru
#                 Bengaluru TO Kolkata
#                 Guwahati TO Delhi
#                 Delhi  TO Kolkata
#                 Chandigarh TO Gurgaon 
#                 Gurgaon TO Hydrabad
#                 Benglore TO Ahmedabad
#                 Surat TO Delhi
#                 Gurgaon TO Ahmedabad


# ================================================================================
# CODE CELL 284
# ================================================================================

Busiest_and_Longest_Routes_top25["Route"] = Busiest_and_Longest_Routes_top25["source_cities"].str.split(" ").apply(lambda x:x[0]) + " TO " + Busiest_and_Longest_Routes_top25["destination_cities"].str.split(" ").apply(lambda x:x[-1])


# ================================================================================
# CODE CELL 285
# ================================================================================

Busiest_and_Longest_Routes_top25.drop(["source_cities","destination_cities"],axis = 1,inplace=True)


# ================================================================================
# CODE CELL 286
# ================================================================================

plt.figure(figsize=(18,7))

plt.subplot(121)
plt.title("Number of trips per route")
sns.barplot(x=Busiest_and_Longest_Routes_top25["Route"],
           y = Busiest_and_Longest_Routes_top25["Number_of_Trips"])
plt.xticks(rotation = 90)
plt.subplot(122)
plt.title("Routes as per Distances between source and destination locations")
sns.barplot(x=Busiest_and_Longest_Routes_top25["Route"],
           y= Busiest_and_Longest_Routes_top25["Average_Actual_distance_to_destination"])
plt.xticks(rotation = 90)
plt.show()


# ================================================================================
# MARKDOWN CELL 287
# ================================================================================
# #### Above charts showing the routes (souce and destinations locations with higest trips between locations) and having long distances.


# ================================================================================
# CODE CELL 288
# ================================================================================




# ================================================================================
# CODE CELL 289
# ================================================================================

route_records.columns


# ================================================================================
# MARKDOWN CELL 290
# ================================================================================
# ## Routes : passing through maxinum number of cities : 


# ================================================================================
# CODE CELL 291
# ================================================================================

route_records[["SouceToDestination_city","Number_of_Trips",
               "Average_Actual_distance_to_destination",
               "#source_cities",
               "#destination_cities"]].sort_values(by=["#source_cities",
                                                       "#destination_cities",
                                                       "Number_of_Trips"]
                                                   ,ascending=False).head(25)


# ================================================================================
# CODE CELL 292
# ================================================================================




# ================================================================================
# CODE CELL 293
# ================================================================================




# ================================================================================
# CODE CELL 294
# ================================================================================




# ================================================================================
# CODE CELL 295
# ================================================================================




# ================================================================================
# MARKDOWN CELL 296
# ================================================================================
# ### Top 20 Longest Route as per : average actual time taken from one city to another city :


# ================================================================================
# CODE CELL 297
# ================================================================================

Longest_route_as_per_actual_trip_time = trip_records.groupby(["source_city",
                      "destination_city"])["actual_time"].mean().sort_values(ascending=False).head(20).reset_index()
Longest_route_as_per_actual_trip_time["route"] = Longest_route_as_per_actual_trip_time["source_city"] + " " + Longest_route_as_per_actual_trip_time["destination_city"]
Longest_route_as_per_actual_trip_time.drop(["source_city",
                                            "destination_city"],axis = 1,inplace=True)
Longest_route_as_per_actual_trip_time
plt.figure(figsize=(11,7))
sns.barplot(y = Longest_route_as_per_actual_trip_time["route"],
           x = Longest_route_as_per_actual_trip_time["actual_time"],)
plt.title("highest number of orders between/within two states")
plt.show()


# ================================================================================
# CODE CELL 298
# ================================================================================




# ================================================================================
# MARKDOWN CELL 299
# ================================================================================
# ### highest number  of Trips happening between/within  two states : 


# ================================================================================
# CODE CELL 300
# ================================================================================

highest_order_between_states = data.groupby(["source_state",
                                             "destination_state"])["trip_uuid"].nunique().sort_values(ascending=False).reset_index()


# ================================================================================
# CODE CELL 301
# ================================================================================

HOBS  = highest_order_between_states.head(15)
HOBS["souce-destination"] = HOBS["source_state"] + " - " + HOBS["destination_state"]
HOBS.drop(["source_state","destination_state"],axis = 1, inplace=True)
HOBS.columns = ["Number_of_trips_between_states","souce-destination_state"] 

plt.figure(figsize=(11,5))
sns.barplot(y = HOBS["souce-destination_state"],
           x = HOBS["Number_of_trips_between_states"],)
plt.title("highest number of orders within two states")
plt.show()


# ================================================================================
# CODE CELL 302
# ================================================================================

HOBS = data.groupby(["source_state","destination_state"])["trip_uuid"].nunique().sort_values(ascending=False).reset_index()
HOBS = HOBS[HOBS["source_state"]!=HOBS["destination_state"]].head(20)

HOBS["souce-destination"] = HOBS["source_state"] + " - " + HOBS["destination_state"]
HOBS.drop(["source_state","destination_state"],axis = 1, inplace=True)
HOBS.columns = ["Number_of_trips_between_states","souce-destination_state"] 

plt.figure(figsize=(11,5))
sns.barplot(y = HOBS["souce-destination_state"],
           x = HOBS["Number_of_trips_between_states"],)
plt.title("highest number of orders between two states")
plt.show()


# ================================================================================
# MARKDOWN CELL 303
# ================================================================================
# > ##### From above charts , 
#         > Delhi to Haryana is the busiest route, having more than 400 trips in between. Some of such busy routes are Haryana to Uttar Pradesh , Chandigarh to Punjab , Delhi to Uttar Pradesh . 
#         > Within the state , Maharashtra , Karnataka, Tamil Nadu are some states having above 1000 trips. 
# 


# ================================================================================
# MARKDOWN CELL 304
# ================================================================================
# ### Top 20 warehouses with heavy traffic : 


# ================================================================================
# CODE CELL 305
# ================================================================================

destination_traffic = data.groupby(["destination_city_state"])["trip_uuid"].nunique().reset_index()
source_traffic = data.groupby(["source_city_state"])["trip_uuid"].nunique().reset_index()
transactions = source_traffic.merge(destination_traffic,
                               left_on="source_city_state"
                               ,right_on="destination_city_state")
transactions.columns = ["source_city_state","#Trips_s","destination_city_state","#Trips_d"]
transactions["TripsTraffic"] = transactions["#Trips_s"]+transactions["#Trips_d"]
transactions.drop(["#Trips_s","#Trips_d","destination_city_state"],axis = 1,inplace=True)
transactions.columns = ["Warehouse_City(Junction)","TripsTraffic"]


# ================================================================================
# CODE CELL 306
# ================================================================================

T = transactions.sort_values(by=["TripsTraffic"],ascending=False).head(20)


# ================================================================================
# CODE CELL 307
# ================================================================================

plt.figure(figsize=(11,8))
sns.barplot(y = T["Warehouse_City(Junction)"],
           x = T["TripsTraffic"])
plt.title("Trips Traffic per Warehouse(for particular city)")
plt.show()


# ================================================================================
# MARKDOWN CELL 308
# ================================================================================
# > #### Top 20 Busiest Warehouse (junctions) as per trips traffic at the juction : are
#  'Bengaluru Karnataka',
#  'Gurgaon Haryana',
#  'Mumbai Maharashtra',
#  'Bhiwandi Maharashtra',
#  'Hyderabad Telangana',
#  'Delhi Delhi',
#  'Pune Maharashtra',
#  'Chandigarh Punjab',
#  'Chennai Tamil Nadu',
#  'Sonipat Haryana',
#  'Kolkata West Bengal',
#  'Ahmedabad Gujarat',
#  'MAA Tamil Nadu',
#  'Jaipur Rajasthan',
#  'Kanpur Uttar Pradesh',
#  'Surat Gujarat',
#  'Muzaffrpur Bihar',
#  'FBD Haryana',
#  'Bhopal Madhya Pradesh',
#  'Noida Uttar Pradesh'
#         


# ================================================================================
# CODE CELL 309
# ================================================================================

trip_records.groupby(["source_state","destination_state"])["trip_uuid"].count().sort_values(ascending=False).head(15).reset_index()


# ================================================================================
# CODE CELL 310
# ================================================================================




# ================================================================================
# MARKDOWN CELL 311
# ================================================================================
# # Inferences and Recommendations : 


# ================================================================================
# MARKDOWN CELL 312
# ================================================================================
# ### Insights and Observations : 
# 
# - 14817 different trips happened between source to destinations during 2018 , September and October.
# - 1504 delivery routes on which trips are happenig.
# - we have 1508 unique source centers and 1481 unique destination centers
# 
# 
# - From 14817 total different trips , we have  8908 (60%) of the trip-routes are Carting , which consists of small vehicles and 5909 (40%) of total trip-routes are FTL : which are Full Truck Load get to the destination sooner. as no other pickups or drop offs along the way .
# 
# - #### Hypothesis tests Results : (In.[52] to In.[89])
#     from 2 sample t-test ,we can also conclude that 
#     
#     - Average time_taken_btwn_odstart_and_od_end for population is equal to Average start_scan_to_end_scan for population.
# 
#     - population average actual_time is less than population average start_scan_to_end_scan.
# 
#     - population mean Actual time taken to complete delivery and population mean time_taken_btwn_od_start_and_od_end are also not same.
# 
#     - Mean of actual time is higher than Mean of the OSRM estimated time for delivery
# 
#     - Population average for Actual Time taken to complete delivery trip and segment actual time are same.
# 
#     - Average of OSRM Time & segment-osrm-time for population is not same.
#     
#     - Population Mean osrm time is less than Population Mean segment osrm time.
# 
#     - Average of OSRM distance for population is less than average of segment OSRM distance
# 
#     - population OSRM estimated distance is higher than the actual distance from source to destination warehouse.
# 
# 
# 
# 
# - #### From Exploratory Data Analysis ( Cells In.[154] to In.[172] )
# 
# 
# - we can observe that Mumbai Maharashtra ,Delhi , Gurgaon(Haryana),Bengaluru Karnataka ,Hyderabad Telangana, Chennai Tamil Nadu, Ahmedabad-Gujarat, Pune Maharashtra, Chandigarh Chandigarh and Kolkata West Bengal are some cities have higest amount of trips happening states with in the city. 
# - If we talk about , not having equal source and destination states , source and destination cities having higest number of trips in between are : Delhi TO Gurgao ,  Gurgaon  TO Bengaluru ,  Bhiwandi/Mumbai TO Pune Maharashtra ,    Sonipat TO    Gurgaon,Haryana
# - It is also been observed that lots of deliveries are happening to airpots  like : Chennai to MAA chennai international Airport , Pune to Pune Airport (PNQ),Kolkata to    CCU West Bengal Kolkata International Airport , Bengluru to BLR-Bengaluru International Airport etc. 
# 
# 
# 
# - From Bar charts , and calculated tables in analysis , we can observe that higest trips are happening is with in the particular cities, in terms of average distance between destinations , we can observe Guwahati to Mumbai , Benglore to Chandigarh ,Benglore to Delhi , Benglore to Gurgaon are the longest routes.
# 
# - #### the souce to destination city routes having largest numbers of trip happening having large distnaces :In[160-163] : 
#     - Guwahati TO Bhiwandi, Bengaluru TO Chandigarh, Bengaluru TO Delhi,Gurgaon TO MAA Chennai Airport,Bhiwandi TO Kolkata, Bengaluru TO Kolkata, Gurgaon TO Hyderabad, Gurgaon TO Kolkata
# 
# 
# - #### the routes which covered multiple cities in between source and destination :
#     - Most covered cities routes are : Guwahati TO LakhimpurN , Jaipur TO Tarnau , Guwahati TO Tura , Mangalore TO Udupi , Ajmer TO Raipur , Mainpuri TO Tilhar . which passes through  more than 8 cities.
# 
# - #### Routes which are busiest from source to destinations and states in which highest activities are noticed :
#     - Delhi to Haryana is the busiest route, having more than 400 trips in between. Some of such busy routes are Haryana to Uttar Pradesh , Chandigarh to Punjab , Delhi to Uttar Pradesh . 
#     - Within the state , Maharashtra , Karnataka, Tamil Nadu, Haryana, Telangana, Gujarat , West Benglore and Uttar Pradesh are some states having above 1000 trips. (In.[173])
# 
# 
# - #### From above chart( In.[172] ) are some warehouse having Maximum traffic and hence busiest junctions. 
#     - Bengaluru Karnataka, Gurgaon Haryana, Mumbai Maharashtra, Hyderabad Telangana, Delhi, Pune Maharashtra, Chandigarh Punjab, Chennai Tamil Nadu, Sonipat Haryana, Kolkata West Bengal, Ahmedabad Gujarat, MAA Tamil Nadu, Jaipur Rajasthan, Kanpur Uttar Pradesh, Surat Gujarat, Muzaffrpur Bihar, FBD Haryana, Bhopal Madhya Pradesh, Noida Uttar Pradesh.
# 
# ### Recommendations : 
# 
# - As per analysis, It is recommended to use Carting (small vehicles) for delivery with in the city in order to reduce the delivery time, and Heavy trucks for long distance trips or heavy load. based on this , we can optimize the delivery time as well as increase the revenue as per requirements. 
# - Incresing the connectivity in tier 2 and tier 3 cities along with profession tie-ups with several e-commerce giants can increase the revenue as well as the reputation on connectivity across borders. 
# - We can work on  optimizing the scanning time on both ends which is start scanning time and end scanning time so that the delivery time can be equated to the OSRM estimated delivery time.
# 
# 


# ================================================================================
# MARKDOWN CELL 313
# ================================================================================
#  ##### Thank you


# ================================================================================
# CODE CELL 314
# ================================================================================



