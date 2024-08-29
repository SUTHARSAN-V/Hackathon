from flask import Flask, request, render_template, jsonify, send_file
from file_handler import extract_text_from_file
from preprocessing import preprocess_text
from text_processing import extract_information
import io
import os
import json
import pandas as pd
from fpdf import FPDF

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Single File Upload Route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error="No file part")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error="No selected file")
    
    if file and (file.filename.endswith('.txt') or file.filename.endswith('.pdf')):
        file_content = io.BytesIO(file.read())
        
        # Save file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, 'wb') as temp_file:
            temp_file.write(file_content.getbuffer())
        
        try:
            text = extract_text_from_file(temp_path)
            cleaned_text = preprocess_text(text)
            information = extract_information(cleaned_text)
            
            # Save JSON result
            json_path = temp_path.replace('temp_', '').replace('.txt', '.json').replace('.pdf', '.json')
            with open(json_path, 'w') as json_file:
                json.dump(information, json_file, indent=4)
            
            # Clean up temporary file
            os.remove(temp_path)
            
            return render_template('single_result.html', filename=file.filename, information=information, json_path=json_path)
        except ValueError as e:
            return render_template('index.html', error=str(e))
    
    return render_template('index.html', error="Unsupported file type")

# Bulk File Upload Route
@app.route('/bulk-upload', methods=['POST'])
def bulk_upload_file():
    if 'files' not in request.files:
        return render_template('index.html', error="No file part")
    
    files = request.files.getlist('files')
    all_information = []
    bulk_json_path = "bulk_analysis.json"

    for file in files:
        if file.filename.endswith('.txt') or file.filename.endswith('.pdf'):
            file_content = io.BytesIO(file.read())
            
            # Save file temporarily
            temp_path = f"temp_{file.filename}"
            with open(temp_path, 'wb') as temp_file:
                temp_file.write(file_content.getbuffer())
            
            try:
                text = extract_text_from_file(temp_path)
                cleaned_text = preprocess_text(text)
                information = extract_information(cleaned_text)
                all_information.append(information)
                
                # Clean up temporary file
                os.remove(temp_path)
            except ValueError as e:
                return render_template('index.html', error=str(e))
    
    # Save combined JSON result
    with open(bulk_json_path, 'w') as bulk_json_file:
        json.dump(all_information, bulk_json_file, indent=4)
    
    return render_template('bulk_results.html', all_information=all_information, bulk_json_path=bulk_json_path)

# CSV Export Route
@app.route('/export/csv/<json_path>', methods=['GET'])
def export_csv(json_path):
    # Load the JSON data
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    # Convert JSON to DataFrame
    df = pd.json_normalize(data)
    
    # Save as CSV
    csv_path = json_path.replace('.json', '.csv')
    df.to_csv(csv_path, index=False)
    
    return send_file(csv_path, as_attachment=True)

# PDF Export Route
@app.route('/export/pdf/<json_path>', methods=['GET'])
def export_pdf(json_path):
    # Load the JSON data
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()
    
    # Add content to PDF
    pdf.set_font("Arial", size=12)
    for item in data:
        for key, value in item.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
        pdf.ln(10)
    
    # Save PDF
    pdf_path = json_path.replace('.json', '.pdf')
    pdf.output(pdf_path)
    
    return send_file(pdf_path, as_attachment=True)

# Graph Analysis Route
@app.route('/analyze-graphs', methods=['POST'])
def analyze_graphs():
    # Placeholder for graph analysis logic
    graph_file = "graphs/analysis.pdf"  # Assuming the graph is saved as a PDF
    # Save or generate the graph and store its path in the graph_file variable
    
    return render_template('bulk_results.html', graph_file=graph_file)

# Download Route
@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
