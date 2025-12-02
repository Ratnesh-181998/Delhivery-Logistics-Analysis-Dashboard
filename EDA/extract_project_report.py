import fitz  # PyMuPDF
import sys

# Set UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'C:\Users\rattu\Downloads\Delhivery\Project_report_Delhivery.pdf'

# Open the PDF
try:
    doc = fitz.open(pdf_path)
    
    full_text = []
    total_pages = len(doc)
    
    # Extract text from all pages
    for page_num in range(total_pages):
        page = doc[page_num]
        page_header = f"\n{'='*80}\nPAGE {page_num + 1} of {total_pages}\n{'='*80}\n"
        full_text.append(page_header)
        
        text = page.get_text()
        if text.strip():
            full_text.append(text)
        else:
            full_text.append("[No text content found on this page]")
    
    doc.close()
    
    # Save to file
    output_file = r'C:\Users\rattu\Downloads\Delhivery\project_report_content.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(full_text))
    
    print(f"PDF content extracted successfully to: {output_file}")
    print(f"Total pages: {total_pages}")

except Exception as e:
    print(f"Error extracting PDF: {e}")
