# 🚚 Delhivery Logistics Analysis Dashboard

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard/graphs/commit-activity)

**An end-to-end interactive analytics solution for optimizing logistics operations through advanced statistical analysis, feature engineering, and real-time visualizations.**

[Live Demo](https://your-app-url.streamlit.app) • [Report Bug](https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard/issues) • [Request Feature](https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard/issues)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [UI Sections](#-ui-sections)
- [Use Cases](#-use-cases)
- [Installation](#-installation)
- [Usage](#-usage)
- [Data Requirements](#-data-requirements)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

The **Delhivery Logistics Analysis Dashboard** is a comprehensive data analytics platform designed to optimize delivery operations for one of India's largest logistics companies. Built with Streamlit and powered by advanced statistical methods, this dashboard transforms raw segment-level logistics data into actionable insights through interactive visualizations and hypothesis testing.

### 🌟 Highlights

- **Real-time Analytics**: Process and visualize logistics data with sub-second response times
- **Statistical Validation**: Hypothesis testing with 95% confidence intervals
- **OSRM Integration**: Compare actual vs estimated delivery metrics
- **Production-Ready**: Comprehensive logging, error handling, and monitoring
- **Scalable Architecture**: Handles datasets with 100K+ records efficiently
  
---
## 🎬 Demo
- **Streamlit Profile** - https://share.streamlit.io/user/ratnesh-181998
- **Project Demo** - https://delhivery-logistics-analysis-dashboard-bp5ruz5asyrx4yc67j5h4i.streamlit.app/

---

## ✨ Key Features

### 📊 **Interactive Exploratory Data Analysis**
- **Overview Dashboard** - Statistical summaries and data structure insights
- **Route Analysis** - FTL vs Carting performance comparison with visualizations
- **Temporal Patterns** - Daily and monthly trend analysis with peak detection
- **Location Analysis** - Geographic distribution across source and destination states
- **Correlation Heatmaps** - Feature relationship visualization with significance levels

### 🛠️ **Advanced Feature Engineering Pipeline**
- **Trip Aggregation** - Transform segment-level to trip-level data with validation
- **Outlier Detection** - IQR-based anomaly identification with 1.5×IQR threshold
- **Feature Scaling** - StandardScaler and MinMaxScaler with before/after comparison
- **One-Hot Encoding** - Categorical variable transformation for ML readiness
- **OSRM Comparison** - Scatter plots with trendlines for actual vs estimated metrics

### 🔬 **Statistical Hypothesis Testing**
- **T-Tests** - Independent samples t-tests for time and distance metrics
- **Significance Testing** - Validate routing engine accuracy (α = 0.05)
- **Distribution Analysis** - Histograms, box plots, violin plots, and scatter plots
- **Summary Dashboard** - Consolidated test results with interpretations
- **Visual Validation** - Color-coded results with statistical significance indicators

### 💡 **Business Insights & Recommendations**
- **Data-Driven Metrics** - Time delays, distance variance, route efficiency KPIs
- **Priority-Based Actions** - High/Medium/Low impact recommendations with timelines
- **ROI Analysis** - Cost-benefit visualization for each recommendation
- **90-Day Action Plan** - Phased implementation roadmap with milestones
- **Impact Estimation** - Projected cost savings and efficiency gains

### 📝 **Advanced Logging & Monitoring**
- **Real-Time Monitoring** - Track all application events with timestamps
- **Log Filtering** - Filter by level (INFO/WARNING/ERROR/DEBUG)
- **Search Functionality** - Keyword-based log search with highlighting
- **Export Options** - Download logs in TXT or CSV format
- **Statistics Dashboard** - Log count by severity level

---

## 🛠️ Tech Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Frontend Framework** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) |
| **Data Processing** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white) |
| **Visualization** | ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge) ![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge) |
| **Statistical Analysis** | ![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white) |
| **Machine Learning** | ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |

</div>

### Core Dependencies

```
streamlit==1.28.0          # Web application framework
pandas==2.0.3              # Data manipulation and analysis
numpy==1.24.3              # Numerical computing
plotly==5.17.0             # Interactive visualizations
matplotlib==3.7.2          # Static plotting
seaborn==0.12.2            # Statistical data visualization
scipy==1.11.2              # Scientific computing and statistics
scikit-learn==1.3.0        # Machine learning utilities
openpyxl==3.1.2            # Excel file support
```

---

## 🖥️ UI Sections

### 1️⃣ **Problem Statement**
**Purpose**: Introduce the business context and challenges

**Features**:
- Hero section with Delhivery branding and gradient background
- Key metrics cards (Total Trips, States Covered, Avg Delivery Time, Route Types)
- About Delhivery company overview
- Business challenges and objectives
- Business impact section (Cost Reduction, Efficiency, Forecasting)
- Collapsible raw data preview

**Visual Elements**: Metric cards, two-column layout, styled containers

---

### 2️⃣ **Solution Approach & Methodology**
**Purpose**: Explain the data processing pipeline and analytical approach

**Features**:
- Visual workflow diagram using Graphviz (Raw Data → Cleaning → Feature Engineering → Aggregation → Outliers → Hypothesis Testing → Insights)
- Grid layout for methodology steps
- Detailed step-by-step process cards
- Feature engineering strategy explanation

**Visual Elements**: Flowchart, grid cards, color-coded sections

---

### 3️⃣ **Interactive Exploratory Data Analysis**
**Purpose**: Deep dive into data patterns and distributions

**Sub-sections** (5 tabs):

#### 📊 Overview
- Numerical features summary statistics
- Categorical features breakdown
- Data quality metrics

#### 🚚 Route Analysis
- Route type distribution (Pie chart)
- Average time by route type (Bar chart)
- FTL vs Carting comparison

#### ⏰ Temporal Patterns
- Trips by day of week (Bar chart)
- Trips by month (Bar chart with trend)
- Peak period identification

#### 📍 Location Analysis
- Top 10 source states (Bar chart)
- Top 10 destination states (Bar chart)
- Geographic concentration insights

#### 🔥 Correlations
- Feature correlation heatmap
- Correlation coefficients (-1 to +1)
- Relationship interpretation guide

**Visual Elements**: Interactive Plotly charts, color-coded heatmaps, tooltips

---

### 4️⃣ **Feature Engineering & Data Processing**
**Purpose**: Showcase data transformation and preparation steps

**Sub-sections** (5 tabs):

#### 📊 Aggregation Logic
- Trip aggregation code example
- Data transformation metrics (segments → trips)
- Before/after comparison
- Data reduction percentage

#### 🧹 Outlier Treatment
- IQR method explanation
- Before/after box plots
- Outliers removed statistics
- Distribution comparison

#### 📏 Scaling
- StandardScaler implementation
- Original vs scaled data comparison
- Scaling visualization (box plots)
- Mean=0, Std=1 validation

#### 🔢 One-Hot Encoding
- Categorical to numerical transformation
- Before/after dataframes
- Binary representation explanation

#### 📈 Feature Comparison
- Actual vs OSRM time (Scatter plot with trendline)
- Actual vs OSRM distance (Scatter plot with trendline)
- Perfect prediction reference line
- Correlation analysis

**Visual Elements**: Code blocks, side-by-side comparisons, scatter plots, box plots

---

### 5️⃣ **Hypothesis Testing**
**Purpose**: Statistical validation of OSRM estimates and data quality

**Sub-sections** (5 tabs):

#### ⏱️ Actual vs OSRM Time
- Null hypothesis: Mean Actual Time ≤ Mean OSRM Time
- T-statistic and P-value metrics
- Distribution comparison (Histogram)
- Box plot comparison
- Statistical interpretation

#### 🔄 Actual vs Segment Time
- Aggregation validation test
- Violin plots with mean lines
- Distribution comparison

#### 🔀 OSRM vs Segment OSRM
- Consistency check
- Scatter plot with trendline
- Correlation analysis

#### 📏 Actual vs OSRM Distance
- Distance accuracy assessment
- Histogram comparison
- Box plot comparison
- Pricing implications

#### 📊 Summary
- All tests summary table
- Decision column (Reject/Fail to Reject H0)
- Significance indicators (✅/❌)
- Key statistical findings

**Visual Elements**: Metrics cards, histograms, box plots, violin plots, scatter plots, summary tables

---

### 6️⃣ **Insights & Recommendations**
**Purpose**: Translate analysis into actionable business strategies

**Sub-sections** (4 tabs):

#### 🔍 Key Findings
- Time estimation gap analysis
- Route type performance insights
- Geographic concentration patterns
- Distance accuracy findings
- Impact and root cause analysis

#### 🎯 Recommendations
- 5 priority-ranked action items
- High/Medium/Low priority badges
- Impact estimates (% improvement)
- Implementation timeline
- Effort assessment

#### 📊 Impact Analysis
- Projected ROI by recommendation (Bar chart)
- Implementation cost vs benefit (Scatter plot)
- Cost savings percentages
- Resource allocation guidance

#### 🚀 Action Plan
- 90-day phased implementation
- Month 1: Audit and analysis
- Month 2: Implementation and pilots
- Month 3: Validation and scaling
- Task-by-task breakdown

**Visual Elements**: Metric cards, priority badges, bar charts, scatter plots, timeline cards

---

### 7️⃣ **Complete Analysis & Advanced Analytics**
**Purpose**: Comprehensive statistical insights and data export

**Features**:
- Correlation analysis heatmap
- Top correlations with actual_time
- Detailed statistics table (describe().T)
- Distribution & outlier analysis (3 tabs)
- Download options (Trip Records CSV, Statistical Report, Correlation Matrix)

**Visual Elements**: Heatmaps, tables, box plots, histograms, download buttons

---

### 8️⃣ **Application Logs**
**Purpose**: Real-time monitoring and debugging

**Features**:
- Log statistics (Total, INFO, WARNING, ERROR counts)
- Multi-select filter by log level
- Keyword search functionality
- Show last N logs (10-1000)
- Color-coded log display (Green/Orange/Red)
- Export options (All Logs TXT, Filtered Logs TXT, CSV)

**Visual Elements**: Metric cards, filters, color-coded log entries, download buttons

---

## 💼 Use Cases

### 🎯 **Primary Use Cases**

1. **Route Optimization**
   - Identify inefficient routes causing delays
   - Compare FTL vs Carting performance
   - Optimize route allocation based on distance and time

2. **Delivery Time Prediction**
   - Improve ETA accuracy by analyzing OSRM vs actual times
   - Identify systematic biases in routing engine
   - Calibrate time estimates with buffer factors

3. **Supply Chain Analytics**
   - Understand geographic distribution patterns
   - Identify high-volume hubs for resource allocation
   - Analyze temporal trends for demand forecasting

4. **Fleet Management**
   - Optimize FTL vs Carting allocation
   - Consolidate smaller shipments into FTL
   - Reduce operational costs through better planning

5. **OSRM Validation**
   - Validate routing engine estimates against real-world data
   - Identify distance and time estimation errors
   - Improve pricing accuracy

6. **Operational Insights**
   - Data-driven decision making for hub operations
   - Peak period identification for staffing
   - Bottleneck detection and resolution

### 🏢 **Industry Applications**

- **E-commerce Logistics**: Last-mile delivery optimization
- **Supply Chain Management**: End-to-end visibility and analytics
- **Transportation Planning**: Route and fleet optimization
- **Warehouse Operations**: Hub performance monitoring
- **Customer Service**: Accurate ETA communication

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### Step-by-Step Installation

1. **Clone the repository**
```bash
git clone https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard.git
cd Delhivery-Logistics-Analysis-Dashboard
```

2. **Create a virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Prepare your data**
   - Place your `delhivery_data.csv` file in the project root directory
   - Ensure the CSV has all required columns (see [Data Requirements](#-data-requirements))

5. **Run the application**
```bash
streamlit run app.py
```

6. **Access the dashboard**
   - Open your browser and navigate to `http://localhost:8501`
   - The dashboard will automatically load and process the data

---

## 📖 Usage

### Running Locally

```bash
# Standard run
streamlit run app.py

# Custom port
streamlit run app.py --server.port 8502

# With specific configuration
streamlit run app.py --server.headless true
```

### Navigating the Dashboard

1. **Start with Problem Statement** - Understand the business context
2. **Review Methodology** - Learn about the data processing pipeline
3. **Explore Interactive EDA** - Analyze data patterns and distributions
4. **Check Feature Engineering** - See how data is transformed
5. **Review Hypothesis Tests** - Validate statistical findings
6. **Read Insights** - Get actionable recommendations
7. **Download Reports** - Export data and analysis
8. **Monitor Logs** - Track application events

---

## 📊 Data Requirements

The application expects a CSV file named `delhivery_data.csv` with the following structure:

### Required Columns

| Column Name | Description | Data Type | Example |
|------------|-------------|-----------|---------|
| `trip_uuid` | Unique trip identifier | String | "trip_12345" |
| `actual_time` | Actual delivery time (hours) | Float | 5.5 |
| `osrm_time` | OSRM estimated time (hours) | Float | 4.8 |
| `segment_actual_time` | Segment-level actual time | Float | 2.3 |
| `segment_osrm_time` | Segment-level OSRM time | Float | 2.0 |
| `actual_distance_to_destination` | Actual distance (km) | Float | 125.5 |
| `osrm_distance` | OSRM estimated distance (km) | Float | 130.2 |
| `route_type` | FTL or Carting | String | "FTL" |
| `source_state` | Origin state | String | "Maharashtra" |
| `destination_state` | Destination state | String | "Karnataka" |
| `trip_creation_day` | Day of week | String | "Wednesday" |
| `trip_creation_month` | Month (1-12) | Integer | 6 |

### Data Format Example

```csv
trip_uuid,actual_time,osrm_time,actual_distance_to_destination,osrm_distance,route_type,source_state,destination_state,trip_creation_day,trip_creation_month
trip_001,5.5,4.8,125.5,130.2,FTL,Maharashtra,Karnataka,Wednesday,6
trip_002,3.2,3.0,85.3,88.1,Carting,Delhi,Haryana,Monday,6
```

### Data Quality Guidelines

- ✅ No missing values in critical columns (trip_uuid, actual_time, osrm_time)
- ✅ Positive values for time and distance metrics
- ✅ Valid route_type values: "FTL" or "Carting"
- ✅ Consistent date formats
- ✅ Minimum 1000 records recommended for statistical significance

---

## 📁 Project Structure

```
Delhivery-Logistics-Analysis-Dashboard/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── packages.txt                    # System-level dependencies
├── README.md                       # Project documentation
├── LICENSE                         # MIT License
│
├── .streamlit/
│   └── config.toml                # Streamlit theme and server config
│
├── .gitignore                     # Git ignore rules
│
├── delhivery_data.csv            # Raw data file (not tracked)
├── delhivery_app.log             # Application logs (not tracked)
│
└── assets/                        # Screenshots and images (optional)
    ├── dashboard_preview.png
    ├── eda_section.png
    └── insights_section.png
```

---

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository: `Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard`
   - Set **Main file path**: `app.py`
   - Click "Deploy"

3. **Configuration**
   - Streamlit Cloud will automatically detect `requirements.txt`
   - Custom theme from `.streamlit/config.toml` will be applied
   - App will be available at: `https://your-app-name.streamlit.app`

### Local Production Deployment

```bash
# Using Docker (create Dockerfile first)
docker build -t delhivery-dashboard .
docker run -p 8501:8501 delhivery-dashboard

# Using systemd (Linux)
# Create service file in /etc/systemd/system/delhivery-dashboard.service
```

---

## 📸 Screenshots

<div align="center">

### Dashboard Overview
![Dashboard Overview](https://via.placeholder.com/800x400?text=Dashboard+Overview)

### Interactive EDA
![Interactive EDA](https://via.placeholder.com/800x400?text=Interactive+EDA)

### Hypothesis Testing
![Hypothesis Testing](https://via.placeholder.com/800x400?text=Hypothesis+Testing)

### Insights & Recommendations
![Insights](https://via.placeholder.com/800x400?text=Insights+%26+Recommendations)

</div>

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guidelines for Python code
- Add comments for complex logic
- Update README.md if adding new features
- Test thoroughly before submitting PR
- Include screenshots for UI changes

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
MIT License

Copyright (c) 2025 Ratnesh Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**What this means:**
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No liability
- ❌ No warranty

---

## 📞 Contact

**RATNESH SINGH**

<div align="center">

[![Email](https://img.shields.io/badge/Email-rattudacsit2021gate%40gmail.com-red?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rattudacsit2021gate@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-ratneshkumar1998-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ratneshkumar1998/)
[![GitHub](https://img.shields.io/badge/GitHub-Ratnesh--181998-black?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ratnesh-181998)
[![Phone](https://img.shields.io/badge/Phone-%2B91--947XXXXX46-green?style=for-the-badge&logo=whatsapp&logoColor=white)](tel:+919470000046)

</div>

### Project Links

- 🌐 **Live Demo**: [Streamlit Cloud](https://delhivery-logistics-analysis-dashboard-bp5ruz5asyrx4yc67j5h4i.streamlit.app/)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard/wiki)
- 🐛 **Issue Tracker**: [GitHub Issues](https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard/discussions)

### Get in Touch

For questions, feedback, or collaboration opportunities:

- 📧 **Email**: [rattudacsit2021gate@gmail.com](mailto:rattudacsit2021gate@gmail.com)
- 💼 **LinkedIn**: Connect for professional networking
- 🐙 **GitHub**: Follow for more data science projects
- 📱 **Phone**: Available for project discussions

---

## 🙏 Acknowledgments

- **Delhivery** - For providing the logistics dataset and business context
- **Streamlit** - For the amazing web framework that makes data apps easy
- **Plotly** - For beautiful and interactive visualizations
- **Open Source Community** - For the incredible tools and libraries
- **Contributors** - Thank you to everyone who has contributed to this project

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard&type=Date)](https://star-history.com/#Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard&Date)

---

## 📈 Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard)
![GitHub last commit](https://img.shields.io/github/last-commit/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard)
![GitHub issues](https://img.shields.io/github/issues/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Ratnesh-181998/Delhivery-Logistics-Analysis-Dashboard)

---

<div align="center">

### 🎯 Keywords

`logistics-analytics` • `supply-chain-optimization` • `delivery-prediction` • `route-analysis` • `osrm` • `streamlit-dashboard` • `data-visualization` • `plotly` • `hypothesis-testing` • `feature-engineering` • `python-analytics` • `delivery-time-estimation` • `fleet-management` • `transportation-analytics` • `data-science` • `machine-learning` • `statistical-analysis` • `business-intelligence` • `interactive-dashboard` • `real-time-analytics`

---

**⭐ If you find this project helpful, please consider giving it a star!**

**Made with ❤️ by [Ratnesh Singh](https://github.com/Ratnesh-181998)**

</div>
