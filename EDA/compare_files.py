import json
import re

# Read the notebook to get original cells
with open('Delhivery Final.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Read both Python files
with open('delhivery_analysis.py', 'r', encoding='utf-8') as f:
    new_file_lines = f.readlines()

with open('Delhivery Final.py', 'r', encoding='utf-8') as f:
    old_file_lines = f.readlines()

print("="*80)
print("FILE COMPARISON ANALYSIS")
print("="*80)

print(f"\nNotebook cells: {len(notebook['cells'])}")
print(f"New file (delhivery_analysis.py): {len(new_file_lines)} lines")
print(f"Old file (Delhivery Final.py): {len(old_file_lines)} lines")

# Count code cells in notebook
code_cells = [c for c in notebook['cells'] if c['cell_type'] == 'code']
markdown_cells = [c for c in notebook['cells'] if c['cell_type'] == 'markdown']

print(f"\nNotebook breakdown:")
print(f"  - Code cells: {len(code_cells)}")
print(f"  - Markdown cells: {len(markdown_cells)}")

# Extract code from new file (delhivery_analysis.py)
new_code_blocks = []
current_block = []
in_code_block = False

for line in new_file_lines:
    if '# CODE CELL' in line:
        if current_block:
            new_code_blocks.append(''.join(current_block))
        current_block = []
        in_code_block = True
    elif '# MARKDOWN CELL' in line:
        if current_block:
            new_code_blocks.append(''.join(current_block))
        current_block = []
        in_code_block = False
    elif in_code_block and not line.strip().startswith('#'):
        if line.strip() and not line.strip().startswith('# ==='):
            current_block.append(line)

if current_block:
    new_code_blocks.append(''.join(current_block))

# Extract code from old file (Delhivery Final.py)
old_code_blocks = []
current_block = []
in_code_block = False

for line in old_file_lines:
    if re.match(r'^# In\[.*\]:', line):
        if current_block:
            old_code_blocks.append(''.join(current_block))
        current_block = []
        in_code_block = True
    elif line.strip().startswith('#') and not re.match(r'^# In\[.*\]:', line):
        if in_code_block and current_block:
            old_code_blocks.append(''.join(current_block))
            current_block = []
        in_code_block = False
    elif in_code_block:
        if line.strip() and not line.strip().startswith('#'):
            current_block.append(line)

if current_block:
    old_code_blocks.append(''.join(current_block))

print(f"\nExtracted code blocks:")
print(f"  - New file: {len(new_code_blocks)} code blocks")
print(f"  - Old file: {len(old_code_blocks)} code blocks")

# Compare first few code blocks
print("\n" + "="*80)
print("SAMPLE COMPARISON (First 5 code blocks)")
print("="*80)

for i in range(min(5, len(new_code_blocks), len(old_code_blocks))):
    new_code = new_code_blocks[i].strip()
    old_code = old_code_blocks[i].strip()
    
    match = new_code == old_code
    print(f"\nCode Block {i+1}: {'✓ MATCH' if match else '✗ DIFFERENT'}")
    if not match:
        print(f"  New: {new_code[:100]}...")
        print(f"  Old: {old_code[:100]}...")

# Overall comparison
print("\n" + "="*80)
print("OVERALL COMPARISON")
print("="*80)

matches = 0
differences = 0

for i in range(min(len(new_code_blocks), len(old_code_blocks))):
    if new_code_blocks[i].strip() == old_code_blocks[i].strip():
        matches += 1
    else:
        differences += 1

print(f"\nMatching code blocks: {matches}")
print(f"Different code blocks: {differences}")
print(f"Total compared: {min(len(new_code_blocks), len(old_code_blocks))}")

if len(new_code_blocks) != len(old_code_blocks):
    print(f"\n⚠ WARNING: Different number of code blocks!")
    print(f"  New file has {len(new_code_blocks)} blocks")
    print(f"  Old file has {len(old_code_blocks)} blocks")

# Check for key differences
print("\n" + "="*80)
print("KEY DIFFERENCES")
print("="*80)

# Check for get_ipython() in old file
get_ipython_count = sum(1 for line in old_file_lines if 'get_ipython()' in line)
print(f"\nOld file has {get_ipython_count} lines with 'get_ipython()' (Jupyter-specific)")
print(f"New file has 1 line with '%matplotlib inline' (needs to be removed for standalone)")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)

if matches == min(len(new_code_blocks), len(old_code_blocks)) and len(new_code_blocks) == len(old_code_blocks):
    print("\n✓ Files appear to have matching code content!")
    print("  The main difference is formatting:")
    print("  - Old file uses 'In[X]:' markers")
    print("  - New file uses '# CODE CELL X' markers")
else:
    print(f"\n⚠ Files have some differences:")
    print(f"  - {matches} matching blocks")
    print(f"  - {differences} different blocks")
    print(f"  - Review recommended")
