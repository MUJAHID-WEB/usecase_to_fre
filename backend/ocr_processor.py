import os
import sys
from PIL import Image

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from standalone_ocr import StandaloneOCR

class OCRProcessor:
    def __init__(self):
        self.tesseract_available = TESSERACT_AVAILABLE
        self.standalone_ocr = StandaloneOCR()
        self.setup_tesseract_path()
    
    def setup_tesseract_path(self):
        """Configure Tesseract path for Windows if available"""
        if not self.tesseract_available:
            print("Tesseract not available. Using standalone OCR mode.")
            return
        
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                print(f"Tesseract found at: {path}")
                return
        
        print("Tesseract not found in common locations. Using standalone OCR mode.")
        self.tesseract_available = False
    
    def extract_text(self, image_path):
        """
        Extract text from image using available methods
        """
        try:
            print(f"Processing image: {image_path}")
            
            if self.tesseract_available:
                return self._extract_with_tesseract(image_path)
            else:
                return self._extract_standalone(image_path)
                
        except Exception as e:
            print(f"OCR processing failed: {str(e)}")
            return self.standalone_ocr.extract_text(image_path)
    
    def _extract_with_tesseract(self, image_path):
        """Extract text using Tesseract OCR"""
        try:
            image = Image.open(image_path)
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            custom_config = r'--oem 3 --psm 6'
            extracted_text = pytesseract.image_to_string(image, config=custom_config)
            
            cleaned_text = self.clean_text(extracted_text)
            print(f"Tesseract OCR extracted {len(cleaned_text)} characters")
            return cleaned_text
            
        except Exception as e:
            print(f"Tesseract failed: {str(e)}")
            self.tesseract_available = False
            return self._extract_standalone(image_path)
    
    def _extract_standalone(self, image_path):
        """Extract text using standalone method"""
        print("Using standalone OCR mode with sample data")
        return self.standalone_ocr.extract_text(image_path)
    
    def clean_text(self, text):
        """Clean and format extracted text"""
        if not text or text.isspace():
            return "No text could be extracted from the image. Using sample use case data."
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)
        
        # If text seems too short or doesn't contain use case keywords, use sample
        use_case_keywords = ['use case', 'actor', 'goal', 'flow', 'system', 'user']
        if len(cleaned_text) < 50 or not any(keyword in cleaned_text.lower() for keyword in use_case_keywords):
            print("Extracted text doesn't appear to be a use case. Using sample data.")
            return self.standalone_ocr.extract_text("sample")
        
        return cleaned_text
    
    def is_tesseract_available(self):
        """Check if Tesseract is available"""
        return self.tesseract_available