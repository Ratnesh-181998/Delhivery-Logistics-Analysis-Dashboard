import json

notebook_path = 'Delhivery Final.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
        
    headings = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            source = cell['source']
            if isinstance(source, list):
                source = ''.join(source)
            
            for line in source.split('\n'):
                if line.strip().startswith('#'):
                    headings.append(line.strip())

    print("Extracted Headings:")
    for h in headings:
        print(h)
        
except Exception as e:
    print(f"Error: {e}")
