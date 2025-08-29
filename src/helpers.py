import pandas as pd
import csv
import os
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class PropertyHelper:
    def __init__(self):
        # Get the current script directory and try to find the CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # Go up one level from src/
        
        # Try different paths for the CSV file
        csv_paths = [
            os.path.join(project_root, 'data', 'properties.csv'),  # From project root
            os.path.join(current_dir, '..', 'data', 'properties.csv'),  # Relative from src
            'data/properties.csv',  # Current directory
            '../data/properties.csv'  # Relative path
        ]
        
        self.properties_df = None
        
        for path in csv_paths:
            try:
                if os.path.exists(path):
                    self.properties_df = pd.read_csv(path)
                    print(f"✅ Successfully loaded CSV from: {path}")
                    break
            except Exception as e:
                print(f"❌ Failed to load from {path}: {e}")
                continue
        
        if self.properties_df is None:
            raise FileNotFoundError(f"Could not find properties.csv file. Tried paths: {csv_paths}")
            
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
    def get_property_by_id(self, listing_id):
        """Get property by exact listing_id match"""
        print(f"🔍 Searching for property ID: {listing_id}")
        print(f"Available IDs: {list(self.properties_df['listing_id'])}")
        property_data = self.properties_df[self.properties_df['listing_id'] == listing_id]
        print(f"Found {len(property_data)} matches")
        return property_data.iloc[0] if not property_data.empty else None
    
    def get_property_by_name(self, property_name):
        """Get property by fuzzy name matching"""
        print(f"🔍 Searching for property name: {property_name}")
        print(f"Available names: {list(self.properties_df['property_name'])}")
        property_name = property_name.lower()
        for _, row in self.properties_df.iterrows():
            if property_name in row['property_name'].lower():
                print(f"✅ Found match: {row['property_name']}")
                return row
        print("❌ No matches found")
        return None
    
    def format_property_details(self, property_data):
        """Format property data into a readable template"""
        if property_data is None:
            return "Property not found."
        
        bedrooms_text = f"{property_data['bedrooms']} BHK" if property_data['bedrooms'] > 0 else "Studio"
        template = f"""
{property_data['property_name']} — {bedrooms_text} ({property_data['area_sqft']} sqft) in {property_data['city']}. 
Price: {property_data['price']:,} {property_data['price_currency']}. 
Status: {property_data['availability']}. 
Description: {property_data['short_description']} 
Contact: {property_data['agent_email']}
        """.strip()
        
        return self.polish_with_llm(template)
    
    def polish_with_llm(self, text):
        """Use Groq to polish the response"""
        try:
            completion = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "You are a helpful real estate assistant. Polish this property information to make it sound natural and conversational while keeping all the facts intact."},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=200
            )
            return completion.choices[0].message.content
        except Exception as e:
            return text  # Fallback to original text if API fails
    
    def save_visit_booking(self, name, phone, property_id="", property_name="", user_message=""):
        """Save visit booking to CSV"""
        visit_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'listing_id': property_id,
            'property_name': property_name,
            'name': name,
            'phone': phone,
            'user_message': user_message
        }
        
        # Try different paths for the visits CSV file
        visits_paths = ['data/visits.csv', '../data/visits.csv', 'src/data/visits.csv']
        visits_file = None
        
        for path in visits_paths:
            if os.path.exists(path):
                visits_file = path
                break
        
        if visits_file is None:
            visits_file = 'data/visits.csv'  # Default fallback
        file_exists = os.path.exists(visits_file)
        
        with open(visits_file, 'a', newline='', encoding='utf-8') as file:
            fieldnames = ['timestamp', 'listing_id', 'property_name', 'name', 'phone', 'user_message']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            writer.writerow(visit_data)

class FAQHelper:
    def __init__(self):
        self.faqs = {
            "office location": "Our office is located at 123 Business District, Mumbai, India.",
            "working hours": "We are open Monday to Friday, 9:00 AM to 6:00 PM IST.",
            "contact": "You can reach us at info@zorever.com or call +91-123-456-7890.",
            "about": "Zorever EcomTech Pvt Ltd is a leading real estate technology company helping people find their dream properties.",
            "services": "We offer property buying, selling, renting, and consultation services across major Indian cities."
        }
    
    def get_faq_answer(self, question):
        """Get FAQ answer based on keywords"""
        question_lower = question.lower()
        for key, answer in self.faqs.items():
            if key in question_lower:
                return answer
        return None

def detect_intent(user_input):
    """Detect user intent from input"""
    user_input_lower = user_input.lower()
    
    # Check for booking intent
    booking_keywords = ['book visit', 'schedule visit', 'visit booking', 'book a visit', 'schedule a visit']
    if any(keyword in user_input_lower for keyword in booking_keywords):
        return 'booking'
    
    # Check for property query (contains P followed by digits or property names)
    if 'P0' in user_input.upper() or any(word in user_input_lower for word in ['apartment', 'villa', 'studio', 'office', 'cottage', 'house']):
        return 'property_query'
    
    # Default to FAQ
    return 'faq'
