import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import sys
import json
import io
import contextlib
from scipy import stats

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Page Config
st.set_page_config(
    page_title="Delhivery Logistics Analysis",
    layout="wide",
    page_icon="🚚",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #e2e8f0;
    }
    .block-container {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3 {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    [data-testid="stSidebar"] { background: #0f172a; border-right: 1px solid #1e293b; }
    .stButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); color: white; border-radius: 8px; font-weight: 600;
    }
    .stRadio > label { color: #e2e8f0 !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Helper: Parse Notebook
@st.cache_data
def parse_notebook(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
            
        sections = []
        current_section = {'title': 'Introduction', 'cells': []}
        
        for cell in notebook['cells']:
            source = cell['source']
            if isinstance(source, list):
                source = ''.join(source)
                
            if cell['cell_type'] == 'markdown':
                # Check for headings
                lines = source.split('\n')
                heading = next((line.strip().lstrip('#').strip() for line in lines if line.strip().startswith('#')), None)
                
                if heading:
                    # Start new section
                    if current_section['cells']:
                        sections.append(current_section)
                    current_section = {'title': heading, 'cells': []}
            
            current_section['cells'].append({'type': cell['cell_type'], 'source': source})
            
        if current_section['cells']:
            sections.append(current_section)
            
        return sections
    except Exception as e:
        st.error(f"Error parsing notebook: {e}")
        return []

# Helper: Parse PDF Text
@st.cache_data
def parse_pdf_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading PDF: {e}"

# Global Execution State
if 'exec_state' not in st.session_state:
    st.session_state['exec_state'] = {
        'pd': pd, 'np': np, 'plt': plt, 'sns': sns, 'stats': stats
    }

def execute_cell(code):
    # Capture stdout
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        try:
            # Add implicit print for last line if it's an expression
            lines = code.strip().split('\n')
            if lines and not lines[-1].strip().startswith(('print', 'import', 'from', '#', 'def', 'class', 'if', 'for', 'while', 'try', 'with')):
                # Try to eval the last line
                last_line = lines[-1]
                exec_code = '\n'.join(lines[:-1])
                exec(exec_code, st.session_state['exec_state'])
                result = eval(last_line, st.session_state['exec_state'])
                if result is not None:
                    print(result)
            else:
                exec(code, st.session_state['exec_state'])
        except Exception as e:
            print(f"Error: {e}")
            
    return f.getvalue()

def main():
    st.sidebar.title("📂 Project Navigator")
    st.sidebar.markdown("---")
    st.sidebar.header("📑 Table of Contents")
    
    # Load and Parse Notebook
    sections = parse_notebook("Delhivery Final.ipynb")
    titles = [s['title'] for s in sections]
    
    # Add Project Report as an option at the end
    titles.append("📄 Project Report")
    
    # Sidebar Navigation
    selected_title = st.sidebar.radio("Go to Section:", titles)
    
    if selected_title == "📄 Project Report":
        st.title("📄 Project Report")
        pdf_content = parse_pdf_text("project_report_content.txt")
        st.markdown(pdf_content)
        
    else:
        # Find selected section
        section = next((s for s in sections if s['title'] == selected_title), None)
        
        if section:
            st.title(section['title'])
            
            # Render Cells
            for i, cell in enumerate(section['cells']):
                if cell['type'] == 'markdown':
                    st.markdown(cell['source'])
                elif cell['type'] == 'code':
                    with st.expander(f"Code Cell {i+1}", expanded=True):
                        st.code(cell['source'], language='python')
                        
                        # Execution Controls
                        col1, col2 = st.columns([1, 5])
                        if col1.button("▶ Run", key=f"run_{selected_title}_{i}"):
                            with st.spinner("Executing..."):
                                output = execute_cell(cell['source'])
                                if output:
                                    st.text_area("Output:", output, height=150)
                                
                                # Check for plots
                                if plt.get_fignums():
                                    st.pyplot(plt.gcf())
                                    plt.clf()

    # Logs Tab (Always visible at bottom or separate?)
    with st.expander("📝 Application Logs", expanded=False):
        try:
            with open("app.log", "r") as f:
                st.text(f.read())
        except:
            st.info("No logs yet.")

if __name__ == "__main__":
    main()
