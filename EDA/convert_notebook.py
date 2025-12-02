import json

# Read the notebook
with open('Delhivery Final.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Open output file
with open('delhivery_analysis.py', 'w', encoding='utf-8') as out:
    # Write header
    out.write('"""' + '\n')
    out.write('Delhivery Feature Engineering Analysis\n')
    out.write('Converted from: Delhivery Final.ipynb\n')
    out.write('"""' + '\n\n')
    
    # Process each cell
    for i, cell in enumerate(notebook['cells']):
        cell_type = cell['cell_type']
        
        if cell_type == 'markdown':
            # Write markdown as comments
            out.write(f'\n# {"=" * 80}\n')
            out.write(f'# MARKDOWN CELL {i + 1}\n')
            out.write(f'# {"=" * 80}\n')
            
            # Get markdown content
            source = cell['source']
            if isinstance(source, list):
                source = ''.join(source)
            
            # Write each line as a comment
            for line in source.split('\n'):
                out.write(f'# {line}\n')
            out.write('\n')
            
        elif cell_type == 'code':
            # Write code cells as executable code
            out.write(f'\n# {"=" * 80}\n')
            out.write(f'# CODE CELL {i + 1}\n')
            out.write(f'# {"=" * 80}\n\n')
            
            # Get code content
            source = cell['source']
            if isinstance(source, list):
                source = ''.join(source)
            
            # Write the code
            out.write(source)
            if not source.endswith('\n'):
                out.write('\n')
            out.write('\n')

print("Conversion completed successfully!")
print(f"Total cells processed: {len(notebook['cells'])}")
print("Output file: delhivery_analysis.py")
