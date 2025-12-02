import re

# Read the converted file
with open('delhivery_analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Update dataset filename
content = content.replace('delhivery_data.txt', 'delhivery_data.csv')

# Fix 2: Remove Jupyter magic commands
content = re.sub(r'^\s*get_ipython\(\)\.run_line_magic.*$', '# \g<0>', content, flags=re.MULTILINE)
content = re.sub(r'^\s*%.*$', '# \g<0>', content, flags=re.MULTILINE)

# Fix 3: Add missing import
if 'from scipy import stats' not in content:
    content = content.replace('import numpy as np', 'import numpy as np\nfrom scipy import stats')

# Fix 4: Comment out plotting commands to avoid runtime errors with display/string conversion
# We'll comment out sns.* and plt.* lines
content = re.sub(r'^\s*(sns\.|plt\.).*$', '# \g<0>', content, flags=re.MULTILINE)

# Write the fixed content to a new file
with open('run_analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
    
    # Append summary code
    f.write('\n\n# ==========================================\n')
    f.write('# AUTOMATED ANALYSIS SUMMARY\n')
    f.write('# ==========================================\n')
    f.write('print("\\n" + "="*50)\n')
    f.write('print("DELHIVERY ANALYSIS RESULTS")\n')
    f.write('print("="*50 + "\\n")\n')
    
    f.write('print(f"Dataset Shape: {df.shape}")\n')
    f.write('print(f"Missing Values:\\n{df.isna().sum()[df.isna().sum() > 0]}")\n')
    
    f.write('print("\\nHYPOTHESIS TESTS:")\n')
    f.write('try:\n')
    f.write('    ks_res = stats.ks_2samp(time_taken_btwn_odstart_and_od_end["time_taken_btwn_odstart_and_od_end"], start_scan_to_end_scan["start_scan_to_end_scan"])\n')
    f.write('    print(f"1. Time Taken vs Scan Time (KS Test): {ks_res}")\n')
    f.write('except Exception as e: print(f"Test 1 failed: {e}")\n')
    
    f.write('try:\n')
    f.write('    ks_res2 = stats.ks_2samp(actual_time["actual_time"], start_scan_to_end_scan["start_scan_to_end_scan"])\n')
    f.write('    print(f"2. Actual Time vs Scan Time (KS Test): {ks_res2}")\n')
    f.write('except Exception as e: print(f"Test 2 failed: {e}")\n')
    
    f.write('try:\n')
    f.write('    ks_res3 = stats.ks_2samp(actual_time["actual_time"], osrm_time["osrm_time"])\n')
    f.write('    print(f"3. Actual Time vs OSRM Time (KS Test): {ks_res3}")\n')
    f.write('except Exception as e: print(f"Test 3 failed: {e}")\n')

print("Created run_analysis.py with fixes (plots disabled).")
