import streamlit as st
import os
import sys
import pandas as pd
from datetime import datetime
sys.path.append('src')

from helpers import PropertyHelper, FAQHelper, detect_intent

# Initialize helpers
@st.cache_resource
def load_helpers():
    return PropertyHelper(), FAQHelper()

property_helper, faq_helper = load_helpers()

# Initialize session state
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'booking_state' not in st.session_state:
    st.session_state.booking_state = None
if 'booking_data' not in st.session_state:
    st.session_state.booking_data = {}
if 'messages' not in st.session_state:
    st.session_state.messages = []

def save_user_query(user_info, query, response, property_id="", property_name=""):
    """Save user query and response to visits.csv"""
    try:
        # Get the current script directory and try to find the CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
        
        # Define potential paths for visits.csv
        potential_paths = [
            os.path.join(project_root, 'data', 'visits.csv'),
            os.path.join(current_dir, 'data', 'visits.csv'),
            os.path.join(current_dir, '..', 'data', 'visits.csv'),
            'data/visits.csv'
        ]
        
        visits_file = None
        for path in potential_paths:
            if os.path.exists(path):
                visits_file = path
                break
        
        if visits_file is None:
            st.error("Could not find visits.csv file")
            return
        
        # Create new entry
        new_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'listing_id': property_id,
            'property_name': property_name,
            'name': user_info.get('name', ''),
            'email': user_info.get('email', ''),
            'phone': user_info.get('phone', ''),
            'user_query': query,
            'bot_response': response
        }
        
        # Read existing data or create new DataFrame
        try:
            df = pd.read_csv(visits_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=['timestamp', 'listing_id', 'property_name', 'name', 'email', 'phone', 'user_query', 'bot_response'])
        
        # Add new entry
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        
        # Save back to file
        df.to_csv(visits_file, index=False)
        
    except Exception as e:
        st.error(f"Error saving query: {e}")

# Login Page
if not st.session_state.user_logged_in:
    st.title("🏠 Zorever Real Estate - Login")
    st.write("Please enter your information to access the chatbot")
    
    with st.form("login_form"):
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        email = st.text_input("Email Address *", placeholder="Enter your email address")
        phone = st.text_input("Phone Number *", placeholder="Enter your phone number")
        
        submitted = st.form_submit_button("Start Chatting")
        
        if submitted:
            if name and email and phone:
                st.session_state.user_info = {
                    'name': name,
                    'email': email,
                    'phone': phone
                }
                st.session_state.user_logged_in = True
                st.success("Login successful! Welcome to Zorever Real Estate Chatbot.")
                st.rerun()
            else:
                st.error("Please fill in all required fields.")

# Main Chatbot Interface
else:
    st.title("🏠 Zorever Real Estate Chatbot")
    st.write(f"Welcome, {st.session_state.user_info['name']}! Ask me about properties, book visits, or general FAQs!")
    
    # User info in sidebar
    with st.sidebar:
        st.header("👤 User Information")
        st.write(f"**Name:** {st.session_state.user_info['name']}")
        st.write(f"**Email:** {st.session_state.user_info['email']}")
        st.write(f"**Phone:** {st.session_state.user_info['phone']}")
        
        if st.button("Logout"):
            st.session_state.user_logged_in = False
            st.session_state.user_info = {}
            st.session_state.messages = []
            st.session_state.booking_state = None
            st.session_state.booking_data = {}
            st.rerun()
        
        st.header("💡 Sample Queries")
        st.write("**Property Queries:**")
        st.write("- What is the price of P003?")
        st.write("- Show details for Sunrise Apartments")
        st.write("- Is P007 available?")
        
        st.write("**General FAQs:**")
        st.write("- Where is your office?")
        st.write("- What are your working hours?")
        st.write("- Contact information")
        
        st.write("**Booking:**")
        st.write("- I want to book a visit")
        st.write("- Schedule a visit")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Handle user input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Process user input
        with st.chat_message("assistant"):
            response = ""
            property_id = ""
            property_name = ""
            
            # Handle booking flow
            if st.session_state.booking_state == 'waiting_name':
                st.session_state.booking_data['name'] = prompt
                st.session_state.booking_state = 'waiting_phone'
                response = "Please share your phone number:"
                
            elif st.session_state.booking_state == 'waiting_phone':
                st.session_state.booking_data['phone'] = prompt
                st.session_state.booking_state = 'waiting_property'
                response = "Which property would you like to visit? (You can provide listing ID like P001 or property name, or say 'any' to skip):"
                
            elif st.session_state.booking_state == 'waiting_property':
                if prompt.lower() != 'any':
                    # Try to find property
                    if prompt.upper().startswith('P'):
                        prop = property_helper.get_property_by_id(prompt.upper())
                        if prop is not None:
                            property_id = prompt.upper()
                            property_name = prop['property_name']
                    else:
                        prop = property_helper.get_property_by_name(prompt)
                        if prop is not None:
                            property_id = prop['listing_id']
                            property_name = prop['property_name']
                
                # Save booking
                property_helper.save_visit_booking(
                    name=st.session_state.booking_data['name'],
                    phone=st.session_state.booking_data['phone'],
                    property_id=property_id,
                    property_name=property_name,
                    user_message=f"Visit booking for {property_name or 'any property'}"
                )
                
                response = f"✅ Visit booking confirmed!\n\n**Booking Details:**\n- Name: {st.session_state.booking_data['name']}\n- Phone: {st.session_state.booking_data['phone']}\n- Property: {property_name or 'Any property'}\n\nOur agent will contact you shortly to schedule the visit."
                
                # Reset booking state
                st.session_state.booking_state = None
                st.session_state.booking_data = {}
            
            else:
                # Regular intent detection
                intent = detect_intent(prompt)
                
                if intent == 'booking':
                    st.session_state.booking_state = 'waiting_name'
                    response = "I'll help you book a property visit! Please share your full name:"
                    
                elif intent == 'property_query':
                    # Extract property ID or name from prompt
                    prompt_upper = prompt.upper()
                    property_found = False
                    
                    # Try to find by listing ID first (look for P followed by 3 digits)
                    import re
                    property_ids = re.findall(r'P\d{3}', prompt_upper)
                    
                    for prop_id in property_ids:
                        prop = property_helper.get_property_by_id(prop_id)
                        if prop is not None:
                            response = property_helper.format_property_details(prop)
                            property_id = prop_id
                            property_name = prop['property_name']
                            property_found = True
                            break
                    
                    # If not found by ID, try by name (extract property names from common patterns)
                    if not property_found:
                        # Look for property names after keywords like "price of", "details for", etc.
                        name_patterns = [
                            r'price of (.+?)(?:\?|$)', 
                            r'details for (.+?)(?:\?|$)',
                            r'information about (.+?)(?:\?|$)',
                            r'tell me about (.+?)(?:\?|$)'
                        ]
                        
                        for pattern in name_patterns:
                            matches = re.findall(pattern, prompt, re.IGNORECASE)
                            if matches:
                                prop_name = matches[0].strip()
                                prop = property_helper.get_property_by_name(prop_name)
                                if prop is not None:
                                    response = property_helper.format_property_details(prop)
                                    property_id = prop['listing_id']
                                    property_name = prop['property_name']
                                    property_found = True
                                    break
                    
                    if not property_found:
                        response = "Sorry, I couldn't find that property. Please check the listing ID (like P001) or property name and try again."
                
                else:  # FAQ
                    faq_answer = faq_helper.get_faq_answer(prompt)
                    if faq_answer:
                        response = faq_answer
                    else:
                        response = "I can help you with:\n- Property information (try 'What is the price of P001?')\n- Booking visits (say 'I want to book a visit')\n- General FAQs about office location, working hours, contact info"
            
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Save the query and response to visits.csv
            save_user_query(st.session_state.user_info, prompt, response, property_id, property_name)
