from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from werkzeug.utils import secure_filename

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from ocr_processor import OCRProcessor
from nlp_processor import NLPProcessor
from fr_generator import FRGenerator

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize processors
ocr_processor = OCRProcessor()
nlp_processor = NLPProcessor()
fr_generator = FRGenerator()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create uploads directory if it doesn't exist
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename,
                'filepath': filepath
            }), 200
        else:
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, pdf'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_diagram():
    try:
        data = request.json
        filepath = data.get('filepath')
        model_type = data.get('model_type', 'rule-based')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        print("Step 1: Performing OCR...")
        extracted_text = ocr_processor.extract_text(filepath)
        
        print("Step 2: Performing NLP analysis...")
        use_case_elements = nlp_processor.extract_use_case_elements(extracted_text)
        
        print("Step 3: Generating functional requirements...")
        functional_requirements = fr_generator.generate_requirements(use_case_elements, model_type)
        
        print("Step 4: Generating traceability matrix...")
        trace_matrix = fr_generator.generate_traceability_matrix(use_case_elements, functional_requirements)
        
        return jsonify({
            'success': True,
            'use_case_description': use_case_elements,
            'functional_requirements': functional_requirements,
            'traceability_matrix': trace_matrix,
            'extracted_text': extracted_text
        }), 200
        
    except Exception as e:
        print(f"Processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Use Case to FR Converter API is running'}), 200

if __name__ == '__main__':
    print("Starting Use Case to FR Converter Server...")
    print("Make sure Tesseract OCR is installed on your system")
    app.run(debug=True, port=5000, host='0.0.0.0')