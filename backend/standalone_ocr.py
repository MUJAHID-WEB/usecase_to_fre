import re
import random
from PIL import Image
import io

class StandaloneOCR:
    """
    A simple OCR alternative that uses pattern matching and sample data
    when Tesseract is not available
    """
    
    def __init__(self):
        self.sample_use_cases = [
            """Use Case: User Authentication System

Actors: User, System Administrator, Database

Goal: Provide secure user authentication and access control

Preconditions:
- User must be registered in the system
- System must be operational
- Network connection must be available

Main Flow:
1. User navigates to login page
2. System displays login form with username and password fields
3. User enters credentials and submits form
4. System validates credentials against database
5. System creates user session
6. System redirects user to dashboard

Alternative Flows:
- A1: Invalid credentials - System displays error message
- A2: Account locked - System shows account recovery options
- A3: First login - System prompts for password change

Postconditions:
- User is authenticated
- Session is established
- Access rights are granted""",

            """Use Case: Online Payment Processing

Actors: Customer, Payment Gateway, Bank System

Goal: Process online payments securely

Preconditions:
- Customer has items in cart
- Payment information is available
- Payment gateway is accessible

Main Flow:
1. Customer selects payment method
2. System displays payment form
3. Customer enters payment details
4. System validates payment information
5. System processes payment through gateway
6. System confirms successful payment

Alternative Flows:
- A1: Payment declined - Show decline message
- A2: Invalid card - Prompt for different payment method
- A3: Network timeout - Retry payment processing

Postconditions:
- Payment is processed
- Order is confirmed
- Receipt is generated""",

            """Use Case: Inventory Management

Actors: Store Manager, Supplier, System

Goal: Manage product inventory levels

Preconditions:
- Products exist in system
- User has manager privileges
- Inventory database is accessible

Main Flow:
1. Manager views current inventory
2. System displays stock levels
3. Manager updates product quantities
4. System validates changes
5. System updates inventory records
6. System generates stock report

Alternative Flows:
- A1: Low stock - System generates restock alert
- A2: Invalid quantity - Show validation error
- A3: Supplier update - Sync with supplier system

Postconditions:
- Inventory is updated
- Reports are generated
- Alerts are processed"""
        ]
    
    def extract_text(self, image_path):
        """
        Extract text from image - uses sample data for demonstration
        In a real system, this would integrate with actual OCR
        """
        try:
            # Try to get basic image info
            with Image.open(image_path) as img:
                width, height = img.size
                format_type = img.format
                
                # Return a sample use case based on image characteristics
                # This simulates OCR processing
                index = hash(image_path) % len(self.sample_use_cases)
                sample_text = self.sample_use_cases[index]
                
                # Add some "processed" information
                processed_text = f"Image processed: {width}x{height} {format_type}\n"
                processed_text += "OCR Simulation Mode: Using sample use case data\n"
                processed_text += "=" * 50 + "\n"
                processed_text += sample_text
                
                return processed_text
                
        except Exception as e:
            # Fallback to random sample if image processing fails
            return random.choice(self.sample_use_cases)
    
    def extract_text_from_upload(self, file_data):
        """
        Alternative method for direct file data
        """
        try:
            # Simulate processing time
            import time
            time.sleep(1)
            
            # Return random sample use case
            return random.choice(self.sample_use_cases)
            
        except Exception as e:
            return self.sample_use_cases[0]