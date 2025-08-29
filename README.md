# 🏠 Zorever Real Estate Chatbot

A smart conversational AI chatbot for real estate inquiries, property searches, and booking management. Built with Streamlit and powered by Groq AI. Features a complete login system with user data collection and comprehensive interaction tracking.

## ✨ Features

### 🔐 User Authentication & Data Collection
- **Login System**: Secure login with name, email, and phone number
- **User Session Management**: Persistent user information throughout the session
- **Complete Interaction Tracking**: Every query and response automatically saved
- **User Profile Display**: User information visible in sidebar
- **Logout Functionality**: Secure session termination

### 🏢 Property Management
- **Property Search**: Find properties by ID (P001, P002, etc.) or name
- **Detailed Information**: Get comprehensive property details including price, location, amenities
- **Availability Status**: Check if properties are available, sold, or on request
- **Smart Query Processing**: Natural language understanding for property inquiries

### 📅 Booking System
- **Visit Booking**: Complete booking flow for property visits
- **Contact Management**: Collect visitor information (name, phone)
- **Property Selection**: Choose specific properties or general visits
- **Booking Confirmation**: Automated confirmation with booking details

### ❓ FAQ & Support
- **Office Information**: Location, working hours, contact details
- **Company Information**: About Zorever, services offered
- **General Support**: Help with common real estate queries

### 📊 Data Analytics
- **Interaction Logging**: All user queries and bot responses saved
- **User Analytics**: Track user behavior and preferences
- **Property Interest**: Monitor which properties generate the most queries
- **Visit Bookings**: Complete booking history with user details

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd zorever-assessment
   ```

2. **Create virtual environment**
   ```bash
   python -m venv zorever_env
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   zorever_env\Scripts\activate
   
   # macOS/Linux
   source zorever_env/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

6. **Run the application**
   ```bash
   streamlit run src/app.py
   ```

7. **Access the chatbot**
   Open your browser and go to: `http://localhost:8501`

## 📁 Project Structure

```
zorever-assessment/
├── data/
│   ├── properties.csv          # Property dataset
│   └── visits.csv             # Complete user interaction data
├── src/
│   ├── app.py                 # Main Streamlit app with login system
│   ├── app_debug.py           # Debug version with error handling
│   ├── helpers.py             # Helper functions
│   └── test_app.py            # Simple test application
├── zorever_env/               # Virtual environment
├── requirements.txt           # Python dependencies
├── test_imports.py           # Import testing script
├── test_properties.py        # Property data testing
├── test_booking.py          # Booking system testing
├── README.md                 # This file
└── .env                      # Environment variables
```

## 🎯 Usage Examples

### Login Process
```
1. Enter your full name, email, and phone number
2. Click "Start Chatting" to access the chatbot
3. Your information will be displayed in the sidebar
4. All interactions will be logged with your details
```

### Property Queries
```
User: "What is the price of P003?"
Bot: "Marina Studio — Studio (420 sqft) in Dubai. Price: 95,000 USD. Status: Available..."

User: "Show details for Sunrise Apartments"
Bot: "Sunrise Apartments — 2 BHK (950 sqft) in Dubai. Price: 250,000 USD..."

User: "Is P005 available?"
Bot: "Green Meadows — 3 BHK (1300 sqft) in Bangalore. Price: 320,000 USD. Status: Available..."
```

### Booking Queries
```
User: "I want to book a visit"
Bot: "I'll help you book a property visit! Please share your full name:"
User: "John Doe"
Bot: "Please share your phone number:"
User: "123-456-7890"
Bot: "Which property would you like to visit? (You can provide listing ID like P001 or property name, or say 'any' to skip):"
```

### General FAQs
```
User: "Where is your office?"
Bot: "Our office is located at 123 Business District, Mumbai, India."

User: "What are your working hours?"
Bot: "We are open Monday to Friday, 9:00 AM to 6:00 PM IST."
```

## 🏢 Available Properties

| ID | Property Name | Type | Location | Price (USD) | Status |
|----|---------------|------|----------|-------------|---------|
| P001 | Sunrise Apartments | 2BHK | Dubai | 250,000 | Available |
| P002 | Desert View Villa | 4BHK | Dubai | 1,250,000 | On Request |
| P003 | Marina Studio | Studio | Dubai | 95,000 | Available |
| P004 | City Center Office | Office | Mumbai | 350,000 | Available |
| P005 | Green Meadows | 3BHK | Bangalore | 320,000 | Available |
| P006 | Lakeside Residence | 3BHK | Hyderabad | 410,000 | Available |
| P007 | Old Town Cottage | 2BHK | Jaipur | 120,000 | Sold |
| P008 | TechPark Studio | 1BHK | Pune | 110,000 | Available |
| P009 | Riverfront Villa | 5BHK | Gurgaon | 1,500,000 | Available |
| P010 | Midtown Flat | 2BHK | Kolkata | 185,000 | On Request |
| P011 | Corner Shop | Commercial | Noida | 75,000 | Available |
| P012 | Suburban House | 3BHK | Chennai | 210,000 | Available |

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key for AI-powered responses

### Customizing Properties
Edit `data/properties.csv` to add, modify, or remove properties:
```csv
id,listing_id,property_name,address,city,area_sqft,bedrooms,bathrooms,price,price_currency,property_type,availability,short_description,agent_email
```

### User Interaction Data
The `data/visits.csv` file automatically stores all user interactions:
```csv
timestamp,listing_id,property_name,name,email,phone,user_query,bot_response
```
- **timestamp**: When the interaction occurred
- **listing_id**: Property ID (e.g., P001, P002) if relevant
- **property_name**: Name of the property if relevant
- **name**: User's full name from login
- **email**: User's email address from login
- **phone**: User's phone number from login
- **user_query**: The exact query typed by the user
- **bot_response**: The complete response from the chatbot

### Adding FAQs
Modify the `faqs` dictionary in `src/helpers.py` to add new FAQ entries.

## 🛠️ Development

### Running in Debug Mode
```bash
streamlit run src/app_debug.py
```

### Testing Imports
```bash
python test_imports.py
```

### Testing Property Data
```bash
python test_properties.py
```

### Testing Booking System
```bash
python test_booking.py
```

### Data Analysis
The `visits.csv` file provides rich data for analysis:
- User engagement patterns
- Most popular properties
- Common query types
- Booking conversion rates
- User interaction frequency

## 📦 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **groq**: AI language model integration
- **python-dotenv**: Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`
   - Check Python version compatibility

2. **CSV File Not Found**
   - Verify `data/properties.csv` exists
   - Check file permissions
   - Ensure correct working directory

3. **Groq API Errors**
   - Verify `GROQ_API_KEY` is set in `.env` file
   - Check API key validity
   - Ensure internet connectivity

4. **Streamlit Port Issues**
   - Try different port: `streamlit run src/app.py --server.port 8502`
   - Check if port is already in use

5. **Login Issues**
   - Ensure all required fields are filled
   - Check for special characters in user input
   - Verify email format

### Getting Help
- Check the debug version: `streamlit run src/app_debug.py`
- Review terminal output for error messages
- Verify all dependencies are installed correctly
- Check the `visits.csv` file for data collection issues

## 📊 Data Privacy

- User information is stored locally in `visits.csv`
- No data is transmitted to external servers (except Groq API for responses)
- Users can logout to clear session data
- All interactions are logged for analytics and support purposes

## 📞 Support

For support and questions:
- Email: info@zorever.com
- Phone: +91-123-456-7890
- Office Hours: Monday to Friday, 9:00 AM to 6:00 PM IST

---

**Built with ❤️ by Zorever EcomTech Pvt Ltd**
