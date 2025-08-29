import pandas as pd
import os
from datetime import datetime

def test_booking_system():
    """Test the booking system by simulating a booking"""
    
    # Test data
    test_booking = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'listing_id': 'P003',
        'property_name': 'Marina Studio',
        'name': 'John Doe',
        'phone': '123-456-7890',
        'user_message': 'I want to visit Marina Studio'
    }
    
    # Check if visits.csv exists
    visits_file = 'data/visits.csv'
    
    if os.path.exists(visits_file):
        print(f"✅ {visits_file} exists")
        
        # Read existing data
        try:
            df = pd.read_csv(visits_file)
            print(f"✅ Successfully read {visits_file}")
            print(f"📊 Current bookings: {len(df)}")
            
            if len(df) > 0:
                print("\n📋 Recent bookings:")
                print(df.tail(3).to_string(index=False))
            
        except Exception as e:
            print(f"❌ Error reading {visits_file}: {e}")
    else:
        print(f"❌ {visits_file} not found")
    
    # Test the booking structure
    print(f"\n🧪 Test booking data:")
    for key, value in test_booking.items():
        print(f"  {key}: {value}")
    
    print(f"\n📁 Project structure verification:")
    print(f"  data/properties.csv: {'✅' if os.path.exists('data/properties.csv') else '❌'}")
    print(f"  data/visits.csv: {'✅' if os.path.exists('data/visits.csv') else '❌'}")
    print(f"  src/app.py: {'✅' if os.path.exists('src/app.py') else '❌'}")
    print(f"  src/helpers.py: {'✅' if os.path.exists('src/helpers.py') else '❌'}")
    print(f"  requirements.txt: {'✅' if os.path.exists('requirements.txt') else '❌'}")
    print(f"  README.md: {'✅' if os.path.exists('README.md') else '❌'}")

if __name__ == "__main__":
    test_booking_system()
