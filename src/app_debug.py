import streamlit as st
import os
import sys
sys.path.append('src')

st.title("🏠 Zorever Real Estate Chatbot - Debug")
st.write("Loading...")

try:
    from helpers import PropertyHelper, FAQHelper, detect_intent
    st.write("✅ Helpers imported successfully")
    
    # Initialize helpers
    @st.cache_resource
    def load_helpers():
        return PropertyHelper(), FAQHelper()

    property_helper, faq_helper = load_helpers()
    st.write("✅ Helpers initialized successfully")
    
except Exception as e:
    st.error(f"❌ Error loading helpers: {e}")
    st.stop()

st.write("✅ App loaded successfully!")

# Initialize session state for booking flow
if 'booking_state' not in st.session_state:
    st.session_state.booking_state = None
if 'booking_data' not in st.session_state:
    st.session_state.booking_data = {}

# Chat interface
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.write("Ask me about properties, book visits, or general FAQs!")

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
        try:
            response = ""
            
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
                property_id = ""
                property_name = ""
                
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
                
                response = f"✅ Visit booking confirmed!\nName: {st.session_state.booking_data['name']}\nPhone: {st.session_state.booking_data['phone']}\nProperty: {property_name or 'Any property'}\n\nOur agent will contact you shortly to schedule the visit."
                
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
            
        except Exception as e:
            st.error(f"Error processing message: {e}")

# Sidebar with sample queries
with st.sidebar:
    st.header("Sample Queries")
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
