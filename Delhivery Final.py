#!/usr/bin/env python
# coding: utf-8

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

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import figure
import warnings
warnings.filterwarnings('ignore')
import statsmodels.api as sm
from scipy.stats import norm
from scipy.stats import t
import plotly.express as px


# In[2]:


pd.set_option('display.max_columns', None)


# In[ ]:





# In[3]:


df = pd.read_csv("delhivery_data.txt")


# In[4]:


df.head(5)


# # Understanding shape and structure of data : 

# In[5]:


df.shape


# In[6]:


# 144,867 total Records 
# 24 columns 


# In[7]:


df.info()


# In[8]:


df.isna().sum()


# In[9]:


# features : source_name and destination_name having few missing values


# ## Changing data type for data and time related features : 
# 

# In[10]:


df["od_end_time"] = pd.to_datetime(df["od_end_time"])
df["od_start_time"] = pd.to_datetime(df["od_start_time"])
df["trip_creation_time"] = pd.to_datetime(df["trip_creation_time"])


# ## Extracting Trip Creation Informations from Trip Creation time : 

# In[11]:


df["trip_creation_time"].dt.month_name().value_counts()


# In[12]:


df["trip_creation_time"].dt.year.value_counts()


# In[13]:


# delivery trip data is given from Septemebr and October 2018.


# In[14]:


df["trip_creation_day"] = (df["trip_creation_time"].dt.day_name())
df["trip_creation_month"] = (df["trip_creation_time"].dt.month_name())
df["trip_creation_year"] = (df["trip_creation_time"].dt.year)


# In[15]:


df["trip_creation_day"].value_counts().plot(kind = "bar")


# In[16]:


# wednesday seems to have relatively higher records of data compare to other days . 
df["trip_creation_day"].value_counts(normalize=True)*100


# In[ ]:





# # Understanding the structure : 

# In[17]:


df.nunique()


# ### we have `14817 different trips happended between source to destinations.` 
# ### total ` 1504 delivery routes` we have.
# 
# #### 1508 unique source centers 
# #### 1481 unique destination centres 
# 
# 
# ## There are two different kind of routes are there : 

# In[18]:


df.groupby("trip_uuid")["route_type"].unique().reset_index()["route_type"].apply(lambda x:x[0]).value_counts()


# In[19]:


df.groupby("trip_uuid")["route_type"].unique().reset_index()["route_type"].apply(lambda x:x[0]).value_counts(normalize = True)*100


# In[20]:


routeType_plot= (df.groupby("trip_uuid")["route_type"].unique().reset_index()["route_type"].apply(lambda x:x[0]).value_counts(normalize = True)*100)
routeType_plot


# In[21]:


sns.barplot(x= routeType_plot.index,
           y = routeType_plot)


# #### From `14817 total different trips` , we have 
# #### 8908 `(60%)` of the trip-routes are `Carting` , which consists of small vehicles and 
# #### 5909 `(40%)` of total trip-routes are `FTL` : which are Full Truck Load get to the destination sooner.  as no otther pickups  or drop offs along the way . 

# In[ ]:





# In[ ]:





# In[ ]:





# # Undestanding Features and Feature Engineering  :
# 
# ## Analyzing records for one particular trip id : 
# 

# In[22]:


df[df["trip_uuid"]=="trip-153741093647649320"]


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

# ### Extracting Features like city - place - code -state from source and destination name columns : 

# In[23]:


df["source_city"] = df["source_name"].str.split(" ",n=1,expand=True)[0].str.split("_",n=1,expand=True)[0]
df["source_state"] = df["source_name"].str.split(" ",n=1,expand=True)[1].str.replace("(","").str.replace(")","")

df["destination_city"] = df["destination_name"].str.split(" ",n=1,expand=True)[0].str.split("_",n=1,expand=True)[0]
df["destination_state"] = df["destination_name"].str.split(" ",n=1,expand=True)[1].str.replace("(","").str.replace(")","")


# In[24]:


df["source_place"] = df["source_name"].str.split("_",n=2,expand=True)[1]
df["destination_place"] = df["destination_name"].str.split("_",n=2,expand=True)[1]



# In[ ]:





# In[25]:


df["source_pincode"] = df["source_center"].apply(lambda x : x[3:9] )
df["destination_pincode"] = df["destination_center"].apply(lambda x : x[3:9] )


# In[26]:


df


# 
# ####  Time_taken_btwn_odstart_and_od_end VS start_scan_to_end_scan : 

# In[27]:


df["time_taken_btwn_odstart_and_od_end"] = ((df["od_end_time"]-df["od_start_time"])/pd.Timedelta(1,unit="hour"))


# #### Converting given time duration features into hours . 
#     start_scan_to_end_scan
#     actual_time
#     osrm_time
#     segment_actual_time
#     segment_osrm_time
#     

# 

# In[28]:


df["start_scan_to_end_scan"] = df["start_scan_to_end_scan"]/60
df["actual_time"] = df["actual_time"]/60
df["osrm_time"] = df["osrm_time"]/60
df["segment_actual_time"] = df["segment_actual_time"]/60
df["segment_osrm_time"] = df["segment_osrm_time"]/60


# In[29]:


df


# In[30]:


df.info()


# In[31]:


df.isna().sum()


# In[32]:


df.shape


# ## Data cleaning : 

# In[33]:


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


# In[34]:


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


# In[35]:


df["destination_city"].replace({
    "del":"Delhi"
},inplace=True)
df["source_city"].replace({
    "del":"Delhi"
},inplace=True)


# 
# 

# In[36]:


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


# In[37]:


df["source_city_state"] = df["source_city"] + " " + df["source_state"]
df["destination_city_state"] = df["destination_city"] + " " + df["destination_state"]


# In[38]:


df["source_city_state"].nunique()


# In[39]:


df["destination_city_state"].nunique()


# In[40]:


df["source_state"].nunique()


# In[41]:


df["destination_state"].nunique()


# In[42]:


## Delhivery delivered in approdimately 1250 cities and almost all the states all over in india. 


# In[43]:


data = df.copy()


# In[44]:


data.columns


# In[45]:


# data[["source_city","source_state","destination_city","destination_state","source_city_state","destination_city_state"]].fillna()


# In[46]:


# above data we impute after aggregating as per tripIDs. 


# In[47]:


data.columns


# In[48]:


data.drop(['source_center',"source_name","destination_center","destination_name","cutoff_timestamp"],axis = 1,inplace=True)


# In[49]:


data.drop(["od_end_time","od_start_time"],axis = 1 , inplace=True)


# In[50]:


data


# # Aggregating Data : 

# In[51]:


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


# ****

# # Hypothesis Tests for time durations and distance related features : 
# 

# ****

# ## Analysing TimeTaken Between OdStart and OdEnd time & StartScanToEndScan : 

# > #### H0: Mean of time taken betweenn trip end ans start time = Mean of start and end scan time
# > #### Ha: Mean of time taken betweenn trip end ans start time != Mean of start and end scan time
# 

# In[52]:


plt.figure(figsize=(15,5))
plt.subplot(121)
sns.distplot((time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"]))
plt.subplot(122)
sns.distplot((start_scan_to_end_scan["start_scan_to_end_scan"]))


# In[53]:


# KS-test : checking the distributions how closly equal thy are : 


# In[54]:


stats.ks_2samp(time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"]
               ,start_scan_to_end_scan["start_scan_to_end_scan"])


# In[55]:


for i in range(5):
    print(stats.ttest_ind((time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"].sample(3000))
                ,(start_scan_to_end_scan["start_scan_to_end_scan"].sample(3000))))


# > #### from Kolmogorov–Smirnov test , p-value is 0.9943 , from which we can conclude  tht both the distributions
# 
# > #### (time_taken_btwn_odstart_and_od_end and start_scan_to_end_scan) are closly similar.
# 
# 
# > ####  from 2 sample t-test ,we can also conclude that Average time_taken_btwn_odstart_and_od_end for population is also equal to Average start_scan_to_end_scan for population.

# In[56]:


# also checking mean and standard deviation for timetaken and scan times : 


# In[57]:


time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"].mean(),time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"].std()


# In[58]:


start_scan_to_end_scan["start_scan_to_end_scan"].mean(),start_scan_to_end_scan["start_scan_to_end_scan"].std()


# In[59]:


# variance and means both are closly similar for scan time and trip start and end time taken 


# In[ ]:





# ## Analysing Actual Time taken to complete the delivery  &  start-scan-end-scan

# > #### H0: Mean of start and end scan time <=  Mean of Actual time taken to complete delivery 
# > #### Ha: Mean of start and end scan time  > Mean of Actual time taken to complete delivery
# 

# In[60]:


plt.figure(figsize=(15,5))
plt.subplot(121)
sns.distplot((actual_time["actual_time"]))
plt.subplot(122)
sns.distplot((start_scan_to_end_scan["start_scan_to_end_scan"]))


# In[61]:


stats.ks_2samp(actual_time["actual_time"],start_scan_to_end_scan["start_scan_to_end_scan"])


# In[62]:


for i in range(7):
    print(stats.ttest_ind((actual_time["actual_time"].sample(3000))
                ,(start_scan_to_end_scan["start_scan_to_end_scan"].sample(3000)),alternative="less"))


# > #### from KS test for actual-time and start_scan_to_end_scan distributions are not same.
# 
# > #### from ttest of population average actual_time is less than population average start_scan_to_end_scan.

# In[63]:


actual_time["actual_time"].mean(),actual_time["actual_time"].std()


# In[64]:


start_scan_to_end_scan["start_scan_to_end_scan"].mean(),start_scan_to_end_scan["start_scan_to_end_scan"].std()


# In[ ]:





# ## Analysing Actual Time & TimeTaken between start and end trip time. 

# > #### H0: Mean of Actual time taken to complete delivery =  Mean of time taken betweenn trip end and start time
# > #### Ha: Mean of Actual time taken to complete delivery  !=  Mean of time taken betweenn trip end and start time

# In[65]:


stats.ks_2samp(actual_time["actual_time"],time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"])


# In[66]:


for i in range(5):
    print(stats.ttest_ind((actual_time["actual_time"].sample(1000))
                ,(time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"].sample(1000))))


# > #### from above kstest of distribution and two sample ttest , 
# > #### we can conclude that population mean Actual time taken to complete delivery and population mean time_taken_btwn_od_start_and_od_end are also not same.

# In[ ]:





# ## Analysing  Actual Time   taken to complete delivery from source to destination hub    &   OSRM measured time : 

# > #### H0: Mean of OSRM time  >=  Mean of Actual time taken to complete delivery
# > #### Ha: Mean of OSRM time  <  Mean of Actual time taken to complete delivery 

# In[67]:


plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((actual_time["actual_time"])))
plt.subplot(122)
sns.distplot(((osrm_time["osrm_time"])))


# In[68]:


stats.ks_2samp(actual_time["actual_time"],
               osrm_time["osrm_time"])


# In[69]:


for i in range(5):
    print(stats.ttest_ind(actual_time["actual_time"].sample(5000),
               osrm_time["osrm_time"].sample(5000),alternative='greater'))


# > #### from two sample ttest can conclude , that population mean actual time taken to complete delivert from source to warehouse and orsm estimate mean time for population are not same. 
# > #### actual time is higher than the osrm estimated time for delivery.

# In[70]:


actual_time["actual_time"].mean(),actual_time["actual_time"].std()


# In[71]:


osrm_time["osrm_time"].mean(),osrm_time["osrm_time"].std()


# In[ ]:





# ## Analysing Actual Time taken to complete delivery from source to destination hub & Segment Actual Time :  

# > #### H0: Actual time = segment actual time
# > #### Ha: Actual time != segment actual time

# In[72]:


plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((actual_time["actual_time"])))
plt.subplot(122)
sns.distplot(((segment_actual_time["segment_actual_time"])))


# In[73]:


for i in range(7):
    print(stats.ttest_ind((actual_time["actual_time"].sample(3000)),
                (segment_actual_time["segment_actual_time"].sample(3000))))


# > #### from two sample ttest , we can conclude that
# > #### Population average for
# > #### Actual Time taken to complete delivery trip and segment actual time are same. 
# 

# In[74]:


actual_time["actual_time"].mean(),actual_time["actual_time"].std()


# In[75]:


segment_actual_time["segment_actual_time"].mean(),segment_actual_time["segment_actual_time"].std()


# In[ ]:





# ## Analysing osrm Time  & segment-osrm-time :  

# > #### H0: segment actual time <= OSRM time
# > #### Ha: segment actual time > OSRM time

# In[76]:


plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((osrm_time["osrm_time"])))
plt.subplot(122)
sns.distplot(((segment_osrm_time["segment_osrm_time"])))


# In[77]:


for i in range(7):
    print(stats.ttest_ind((osrm_time["osrm_time"].sample(3000)),
                (segment_osrm_time["segment_osrm_time"].sample(3000)),alternative ="less"))


# > #### from ttest , we can conclude that 
# > #### average of osrm Time & segment-osrm-time for population is not same. 
# > #### Population Mean osrm time  is less than Population Mean segment osrm time.
# 

# In[78]:


osrm_time["osrm_time"].mean(),osrm_time["osrm_time"].std()


# In[79]:


segment_osrm_time["segment_osrm_time"].mean(),segment_osrm_time["segment_osrm_time"].std()


# In[ ]:





# # Analysing Distances measures : 

# ## Analysing and Visulizing OSRM Estimated distance and Segment-osrm-distance  :

# > #### H0 : Segment OSRM distnace <= OSRM distnace
# > #### Ha : Segment OSRM distnace > OSRM distnace

# In[80]:


plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((osrm_distance["osrm_distance"])))
plt.subplot(122)
sns.distplot(((segment_osrm_distance["segment_osrm_distance"])))


# In[81]:


stats.ks_2samp(osrm_distance["osrm_distance"],segment_osrm_distance["segment_osrm_distance"])


# In[82]:


for i in range(7):
    print(stats.ttest_ind(osrm_distance["osrm_distance"].sample(5000),
               segment_osrm_distance["segment_osrm_distance"].sample(5000),alternative="less"))


# 

# In[83]:


osrm_distance["osrm_distance"].mean(),osrm_distance["osrm_distance"].std()


# In[84]:


segment_osrm_distance["segment_osrm_distance"].mean(),segment_osrm_distance["segment_osrm_distance"].std()


# >    #### from KS test , we can conclude the distributions of segment osrm distance and osrm distnace are not same! 
# >    #### from two sample one sided ttest, we can conclude: Average of osrm distance for population is less than  average of segment osrm distnace 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## Analysing and Visulizing OSRM Estimated distance and Actual Distance between source and destination warehouse :

# > #### H0 : Mean OSRM distance <= Mean Actual distnace 
# > #### Ha : Mean OSRM distance > Mean Actual distnace 

# In[85]:


plt.figure(figsize=(10,4))
plt.subplot(121)
sns.distplot(((osrm_distance["osrm_distance"])))
plt.subplot(122)
sns.distplot(((actual_distance_to_destination["actual_distance_to_destination"])))


# In[86]:


stats.ks_2samp(osrm_distance["osrm_distance"],actual_distance_to_destination["actual_distance_to_destination"])


# In[87]:


for i in range(5):
    print(stats.ttest_ind(osrm_distance["osrm_distance"].sample(5000),
               actual_distance_to_destination["actual_distance_to_destination"].sample(5000),alternative="greater"))


# > #### From left sided ttest , we can conclude 
# > #### for population OSRM estimated distance is higher than the actual distance  from source to destination warehouse. 

# In[88]:


osrm_distance["osrm_distance"].mean(),osrm_distance["osrm_distance"].std()


# In[89]:


actual_distance_to_destination["actual_distance_to_destination"].mean(),actual_distance_to_destination["actual_distance_to_destination"].std()


# ****

# ****
# ****

# In[ ]:





# In[ ]:





# In[ ]:





# ****

# # Merging All the numerical Fields as per TripID: 
actual_distance_to_destination
osrm_distance
segment_osrm_distancetime_taken_btwn_odstart_and_od_end
start_scan_to_end_scan
actual_time
segment_actual_time
osrm_time
segment_osrm_time


# In[ ]:





# In[90]:


distances = segment_osrm_distance.merge(actual_distance_to_destination.merge(osrm_distance,
                                                                             on="trip_uuid"),
                                                                            on="trip_uuid")


# In[91]:


time = segment_osrm_time.merge(osrm_time.merge(segment_actual_time.merge(actual_time.merge(time_taken_btwn_odstart_and_od_end.merge(start_scan_to_end_scan,
                                         on="trip_uuid",
                                         ),on="trip_uuid"),on="trip_uuid"),on="trip_uuid"),on="trip_uuid")


# In[92]:


Merge1 = time.merge(distances,on="trip_uuid",
                                        )


# In[ ]:





# In[93]:


Merge1


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# #  Merging Location details and route_type and Numerical data on TripID : 

# In[94]:


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


# In[ ]:





# In[95]:


route_type = data.groupby("trip_uuid")["route_type"].unique().reset_index()


# In[96]:


Merged = route_type.merge(locations.merge(Merge1,on="trip_uuid",
           how="outer"),
                 on="trip_uuid",
           how="outer"
                )


# In[97]:


trip_records = Merged.copy()


# In[98]:


trip_records["route_type"] = trip_records["route_type"].apply(lambda x:x[0])


# In[99]:


route_to_merge = data.groupby("trip_uuid")["route_schedule_uuid"].unique().reset_index()


# In[100]:


trip_records = trip_records.merge(route_to_merge,on="trip_uuid",how="outer")


# In[101]:


trip_records["route_schedule_uuid"] = trip_records["route_schedule_uuid"].apply(lambda x:x[0])


# In[102]:


trip_records


# In[ ]:





# In[ ]:





# In[103]:


# route_df['source'] = route_df['source'].str.strip("{''}")


# In[104]:


trip_records.isna().sum()


# In[ ]:





# In[105]:


trip_records.loc[trip_records.isnull().any(axis=1)]


# In[106]:


trip_records[trip_records["trip_uuid"]=="trip-153852612674280168"]


# In[107]:


trip_records.dropna(axis= 0,how = 'any',inplace = True)


# In[ ]:





# In[108]:


trip_records["source_city"] = trip_records["source_city"].astype("str").str.strip("[]").str.replace("'","")
trip_records["destination_city"] = trip_records["destination_city"].astype("str").str.strip("[]").str.replace("'","")
trip_records["source_city_state"] = trip_records["source_city_state"].astype("str").str.strip("[]").str.replace("'","")
trip_records["destination_city_state"] = trip_records["destination_city_state"].astype("str").str.strip("[]").str.replace("'","")

trip_records["source_state"] = trip_records["source_state"].astype("str").str.strip("[]").str.replace("'","")
trip_records["destination_state"] = trip_records["destination_state"].astype("str").str.strip("[]").str.replace("'","")


# In[ ]:





# In[ ]:





# ### Checking if any null values left in Trip Records Data : 

# In[109]:


trip_records.isna().sum()


# In[ ]:





# In[ ]:





# In[110]:


trip_records.loc[trip_records.isnull().any(axis=1)]


# In[111]:


trip_records.corr()


# In[112]:


trip_records.to_csv("trip_records.csv")


# ## Treating Outliers : 

# In[113]:


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


# In[114]:


outlier_treatment  = trip_records.copy()


# In[115]:


outlier_treatment_num = outlier_treatment[['segment_osrm_time', 'osrm_time',
       'segment_actual_time', 'actual_time',
       'time_taken_btwn_odstart_and_od_end', 'start_scan_to_end_scan',
        'segment_osrm_distance', 'actual_distance_to_destination',
        'osrm_distance']]


# In[ ]:





# In[116]:


# outlier_treatment_num[(np.abs(stats.zscore(outlier_treatment_num)) < 3).all(axis=1)]


# ## After removing outliers from all numerical features :  

# In[117]:


trip_records_without_outliers = trip_records.loc[outlier_treatment_num[(np.abs(stats.zscore(outlier_treatment_num)) < 3).all(axis=1)].index]
trip_records_without_outliers


# In[118]:


trip_records_without_outliers = trip_records_without_outliers[['trip_uuid','route_type','source_city_state', 'destination_city_state','segment_osrm_time', 'osrm_time',
       'segment_actual_time', 'actual_time',
       'time_taken_btwn_odstart_and_od_end', 'start_scan_to_end_scan',
       'segment_osrm_distance', 'actual_distance_to_destination',
       'osrm_distance']]


# In[119]:


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


# In[ ]:





# ## Processing Data for One hot encoding : 
# 
# ### merging locations details into one columns . and re categorise the data as per highest trips having location as top category 
# 

# In[120]:


trip_records_without_outliers["destination_source_locations"] = trip_records_without_outliers["source_city_state"]+" "+trip_records_without_outliers["destination_city_state"]
trip_records_without_outliers.drop(["source_city_state","destination_city_state"],axis = 1,inplace=True)


# In[121]:


sc_dc = trip_records_without_outliers.groupby(["destination_source_locations"])["trip_uuid"].nunique().sort_values(ascending= False).reset_index()


# In[122]:


# trip_records.groupby(['source_state','destination_state'])["trip_uuid"].nunique().sort_values(ascending= False).reset_index().head(30)


# In[123]:


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


# In[124]:


sc_dc["city"]  = pd.Series(map(get_cat,sc_dc["trip_uuid"]))


# In[125]:


trip_records_for_encoding = sc_dc.merge(trip_records_without_outliers,
            on="destination_source_locations")
trip_records_for_encoding.drop(["destination_source_locations","trip_uuid_x"],axis = 1,inplace=True)


# In[126]:


trip_records_for_encoding.drop(["trip_uuid_y"],axis = 1,inplace=True)
# trip_records_for_encoding.sample(15)


# In[127]:


encoded_data = pd.get_dummies(trip_records_for_encoding,
             columns=["route_type","city"] )


# In[128]:


encoded_data


# In[129]:


['segment_osrm_time', 'osrm_time',
       'segment_actual_time', 'actual_time',
       'time_taken_btwn_odstart_and_od_end', 'start_scan_to_end_scan' ,'segment_osrm_distance', 'actual_distance_to_destination','osrm_distance' ]


# In[130]:


from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler


# In[131]:


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


# In[ ]:





# In[132]:


scaler = MinMaxScaler()
MinMax_data = scaler.fit_transform(encoded_data[['segment_osrm_time','osrm_time','segment_actual_time','actual_time',
 'time_taken_btwn_odstart_and_od_end','start_scan_to_end_scan','segment_osrm_distance','actual_distance_to_destination',
 'osrm_distance']])
MinMax_data = pd.DataFrame(MinMax_data,columns=['segment_osrm_time',
 'osrm_time','segment_actual_time','actual_time','time_taken_btwn_odstart_and_od_end','start_scan_to_end_scan',
 'segment_osrm_distance','actual_distance_to_destination','osrm_distance'])
MinMax_data.head()


# In[133]:


std_data


# In[ ]:





# In[134]:


one_hot_encoded_data = encoded_data[["route_type_Carting","route_type_FTL","city_Category 1",
 "city_Category 2","city_Category 3","city_Category 4",
 "city_Category 5","city_Category 6","city_Category 7"]]


# In[135]:


Standardized_Data = pd.concat([std_data,one_hot_encoded_data],axis = 1)


# In[136]:


Min_Max_Scaled_Data = pd.concat([MinMax_data,one_hot_encoded_data],axis = 1)


# In[137]:


Standardized_Data.sample(5)


# In[138]:


Min_Max_Scaled_Data.sample(5)


# In[ ]:





# # Route analysis : 

# In[139]:


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


# In[140]:


I = data.groupby("route_schedule_uuid")[["source_city",
                                         "destination_city"]].nunique().sort_values(by="source_city",
                                                                                     ascending=False).reset_index()
I.columns = ["route_schedule_uuid","#source_cities"
             ,"#destination_cities"]


# In[141]:


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


# In[142]:


# route_records.sort_values(by="Average_Actual_distance_to_destination",ascending=False)


# In[143]:


route_records.isna().sum()


# In[144]:


route_records.dropna(inplace=True)


# In[145]:


route_records["route_type"] = route_records["route_type"].astype("str").str.strip("[]").str.replace("'","")
route_records["source_cities"] = route_records["source_cities"].astype("str").str.strip("[]").str.replace("'","")
route_records["destination_cities"] = route_records["destination_cities"].astype("str").str.strip("[]").str.replace("'","")
route_records["source_states"] = route_records["source_states"].astype("str").str.strip("[]").str.replace("'","")
                             
route_records["destination_states"] = route_records["destination_states"].astype("str").str.strip("[]").str.replace("'","")                        


# In[146]:


route_records


# In[147]:


route_records["ROUTE"] = route_records["source_cities"] + " -- " + route_records["destination_cities"]


# In[148]:


route_records.drop(["route_schedule_uuid"],axis = 1,inplace=True)


# In[149]:


first_column = route_records.pop('ROUTE')
route_records.insert(0, 'ROUTE', first_column) 


# In[150]:


route_records["SouceToDestination_city"] = route_records["source_cities"].str.split(" ").apply(lambda x:x[0]) +" TO " +route_records["destination_cities"].str.split(" ").apply(lambda x:x[-1])


# In[151]:


first_column = route_records.pop('SouceToDestination_city')
route_records.insert(0, 'SouceToDestination_city', first_column) 


# In[152]:


route_records


# In[153]:


route_records.to_csv("route_records.csv")


# In[ ]:





# In[ ]:





# In[ ]:





# ##  Exploratory Data Analysis : ( getting some  insights from preprocessed data ) : 

# In[ ]:





# In[ ]:





# ## Busiest Route Analysis : 
# 

# ### Number of Trips between cities , sorted highest to lowest
# > #### Top 20 source and destination cities wihc have high freqency of trips in between . 

# In[154]:


Number_of_trips_between_cities = data.groupby(["source_city_state",
                                               "destination_city_state"])["trip_uuid"].nunique().sort_values(ascending=False).reset_index()
Number_of_trips_between_cities.head(25)


# > ##### From above table, we can observe that Mumbai Maharashtra ,Delhi ,Gurgaon(Haryana),Bengaluru Karnataka	,Hyderabad Telangana,Chennai Tamil Nadu,Ahmedabad Gujarat,Pune Maharashtra,Chandigarh Chandigarh and Kolkata West Bengal	 are some cities have higest amount of trips happening states with in the city :	

# In[155]:


Number_of_trips_between_cities.loc[Number_of_trips_between_cities["source_city_state"] != Number_of_trips_between_cities["destination_city_state"]].head(25)


# > ##### If we talk about , not having equal source and destination states , source and destination cities having higest number of trips in between are : 
#         delhi to gurgao
#         Gurgaon,Haryana TO Bengaluru,Karnataka
#         Bhiwandi/Mumbai,Maharashtra TO Pune Maharashtra
#         Sonipat TO	Gurgaon,Haryana
#         
#       - it is also been observed that lots of deliveries are happening to airpots 
#       - like : Chennai to MAA chennai international Airport , Pune to Pune Airport (PNQ),Kolkata to	CCU West Bengal Kolkata International Airport , Bengluru to BLR-Bengaluru Internation Airport etc. 
#         

# In[ ]:





# In[ ]:





# In[156]:


route_records[["ROUTE","Number_of_Trips",
               "Average_Actual_distance_to_destination",
               "#source_cities",
               "#destination_cities"]].sort_values(by="Number_of_Trips",ascending=False).head(25)


# #### Top Routes having Maximum Number of Trips between/within the source and destinations . 

# In[157]:


plt.figure(figsize=(12,8))

X = route_records[["ROUTE", "Number_of_Trips",
               ]].sort_values(by="Number_of_Trips",ascending=False).head(35)
sns.barplot(y = X["ROUTE"],
           x= X["Number_of_Trips"])
plt.title("Number of trips per route")
plt.xticks(rotation = 90)
plt.show()


# In[158]:


plt.figure(figsize=(12,8))

X = route_records[["ROUTE", "Average_Actual_distance_to_destination",
               ]].sort_values(by="Average_Actual_distance_to_destination",ascending=False).head(25)
sns.barplot(y = X["ROUTE"],
           x = X["Average_Actual_distance_to_destination"])
plt.xticks(rotation = 90)
plt.show()


# > #### From above Bar chart , and table , we can observe that higest trips are happening is with in the particular cities. 
# > #### in terms of average distnace between destinations , we can observe Guwahati to Mumbai , Benglore to Chandigarh ,Benglore to Delhi  , Benglore to Gurgaon are the longest routes .
# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Busiest and Longest Routes : 

# In[ ]:





# In[159]:


Busiest_and_Longest_Routes  = route_records[(route_records["Average_Actual_distance_to_destination"] > route_records["Average_Actual_distance_to_destination"].quantile(0.75)) 
              & (route_records["Number_of_Trips"] > route_records["Number_of_Trips"].quantile(0.75))].sort_values(by="Average_Actual_distance_to_destination"
                                                                                                                  ,ascending=False)


# In[160]:


Busiest_and_Longest_Routes_top25 = Busiest_and_Longest_Routes[["source_cities",
                                                               "destination_cities",
                                                               "Number_of_Trips",
                                                               "Average_Actual_distance_to_destination"]].head(25)
Busiest_and_Longest_Routes_top25


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

# In[161]:


Busiest_and_Longest_Routes_top25["Route"] = Busiest_and_Longest_Routes_top25["source_cities"].str.split(" ").apply(lambda x:x[0]) + " TO " + Busiest_and_Longest_Routes_top25["destination_cities"].str.split(" ").apply(lambda x:x[-1])


# In[162]:


Busiest_and_Longest_Routes_top25.drop(["source_cities","destination_cities"],axis = 1,inplace=True)


# In[163]:


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


# #### Above charts showing the routes (souce and destinations locations with higest trips between locations) and having long distances.

# In[ ]:





# In[164]:


route_records.columns


# ## Routes : passing through maxinum number of cities : 

# In[165]:


route_records[["SouceToDestination_city","Number_of_Trips",
               "Average_Actual_distance_to_destination",
               "#source_cities",
               "#destination_cities"]].sort_values(by=["#source_cities",
                                                       "#destination_cities",
                                                       "Number_of_Trips"]
                                                   ,ascending=False).head(25)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ### Top 20 Longest Route as per : average actual time taken from one city to another city :

# In[166]:


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


# In[ ]:





# ### highest number  of Trips happening between/within  two states : 

# In[167]:


highest_order_between_states = data.groupby(["source_state",
                                             "destination_state"])["trip_uuid"].nunique().sort_values(ascending=False).reset_index()


# In[168]:


HOBS  = highest_order_between_states.head(15)
HOBS["souce-destination"] = HOBS["source_state"] + " - " + HOBS["destination_state"]
HOBS.drop(["source_state","destination_state"],axis = 1, inplace=True)
HOBS.columns = ["Number_of_trips_between_states","souce-destination_state"] 

plt.figure(figsize=(11,5))
sns.barplot(y = HOBS["souce-destination_state"],
           x = HOBS["Number_of_trips_between_states"],)
plt.title("highest number of orders within two states")
plt.show()


# In[169]:


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


# > ##### From above charts , 
#         > Delhi to Haryana is the busiest route, having more than 400 trips in between. Some of such busy routes are Haryana to Uttar Pradesh , Chandigarh to Punjab , Delhi to Uttar Pradesh . 
#         > Within the state , Maharashtra , Karnataka, Tamil Nadu are some states having above 1000 trips. 
# 

# ### Top 20 warehouses with heavy traffic : 

# In[170]:


destination_traffic = data.groupby(["destination_city_state"])["trip_uuid"].nunique().reset_index()
source_traffic = data.groupby(["source_city_state"])["trip_uuid"].nunique().reset_index()
transactions = source_traffic.merge(destination_traffic,
                               left_on="source_city_state"
                               ,right_on="destination_city_state")
transactions.columns = ["source_city_state","#Trips_s","destination_city_state","#Trips_d"]
transactions["TripsTraffic"] = transactions["#Trips_s"]+transactions["#Trips_d"]
transactions.drop(["#Trips_s","#Trips_d","destination_city_state"],axis = 1,inplace=True)
transactions.columns = ["Warehouse_City(Junction)","TripsTraffic"]


# In[171]:


T = transactions.sort_values(by=["TripsTraffic"],ascending=False).head(20)


# In[172]:


plt.figure(figsize=(11,8))
sns.barplot(y = T["Warehouse_City(Junction)"],
           x = T["TripsTraffic"])
plt.title("Trips Traffic per Warehouse(for particular city)")
plt.show()


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

# In[173]:


trip_records.groupby(["source_state","destination_state"])["trip_uuid"].count().sort_values(ascending=False).head(15).reset_index()


# In[ ]:





# # Inferences and Recommendations : 

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

#  ##### Thank you

# In[ ]:




