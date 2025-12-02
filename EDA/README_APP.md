# Delhivery Logistics Analysis App

This is a polished Streamlit application that provides an interactive interface for the Delhivery Feature Engineering project.

## Features

1.  **Project Navigator (Sidebar):**
    -   Switch between the **Notebook Analysis** (code & insights) and the **Project Report** (PDF content).
    -   Derived dynamically from the source files.

2.  **Interactive Analysis Tabs:**
    -   **Data Overview:** View raw dataset statistics and preview.
    -   **Cleaning & Features:** Execute the full feature engineering pipeline with a single click. View the transformed data.
    -   **EDA:** Visualize trip distributions and route types.
    -   **Hypothesis Testing:** Run statistical tests (T-Test) on demand to compare Actual vs OSRM times.
    -   **Logs:** View real-time application logs.

3.  **Polished Design:**
    -   Dark mode with modern gradients.
    -   Custom CSS for a premium look and feel (similar to LoanTap app).

## How to Run

1.  Ensure you have the required libraries installed:
    ```bash
    pip install streamlit pandas numpy matplotlib seaborn scipy
    ```

2.  Run the application:
    ```bash
    streamlit run delhivery_app.py
    ```

3.  The app will open in your default browser at `http://localhost:8501`.

## Files
-   `delhivery_app.py`: The main Streamlit application.
-   `delhivery_solution.py`: Core analysis logic used by the app.
-   `delhivery_analysis.py`: Converted notebook script used for parsing sections.
-   `project_report_content.txt`: Extracted text from the project report PDF.
