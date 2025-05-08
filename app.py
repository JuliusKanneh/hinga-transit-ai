import streamlit as st
from modules.nlp_parser import parse_farmer_message
from modules.nlp_parser import parse_driver_message
from modules.matching_engine import match_farmer_driver
import dateparser

st.title("Hinga Transit AI")
st.subheader("Message Parser Demo")
st.write("This app parses messages from farmers and drivers to extract relevant information.")

# ---------------------------- Farmer Input Form ----------------------------
st.header("Farmer and Driver Free Text Input")

farmer_message = st.text_area("Enter your message (e.g., 'I have 3 sacks of tomatoes ready by Thursday in Musanze.')")
if 'parsed_farmer' not in st.session_state:
    st.session_state.parsed_farmer = {}

if st.button("Parse Farmer Message"):
    parsed_data = parse_farmer_message(farmer_message)

    # Always add missing keys to avoid KeyError later
    if 'Time Ready' not in parsed_data:
        parsed_data['Time Ready'] = None

    st.session_state.parsed_farmer = parsed_data

    st.write("Parsed Data:")
    st.json(parsed_data)

    if not parsed_data['Date Ready']:
        missing_date = st.text_input("We couldn't find a date in your message. Please enter the day the crops will be ready (e.g., May 10, Thursday, next week):", key="farmer_date")
        if missing_date:
            manual_date = dateparser.parse(missing_date, settings={'PREFER_DATES_FROM': 'future'})
            if manual_date:
                st.session_state.parsed_farmer['Date Ready'] = manual_date.date()
                if not st.session_state.parsed_farmer.get('Time Ready'):
                    st.session_state.parsed_farmer['Time Ready'] = manual_date.time()

    if not st.session_state.parsed_farmer.get('Time Ready'):
        missing_time = st.text_input("Please specify the time the crops will be ready (e.g., 8:00 AM):", key="farmer_time")
        if missing_time:
            manual_time = dateparser.parse(missing_time)
            if manual_time:
                st.session_state.parsed_farmer['Time Ready'] = manual_time.time()

    st.write("Updated Farmer Data after filling missing details:")
    st.json(st.session_state.parsed_farmer)

    # Save to JSON
    import json, os
    if not os.path.exists('farmer_data.json'):
        all_farmers = []
    else:
        with open('farmer_data.json', 'r') as f:
            try:
                all_farmers = json.load(f)
            except json.JSONDecodeError:
                all_farmers = []

    all_farmers.append({
        "Crop": st.session_state.parsed_farmer.get('Crop'),
        "Quantity": st.session_state.parsed_farmer.get('Quantity'),
        "Urgency": st.session_state.parsed_farmer.get('Urgency'),
        "Location": st.session_state.parsed_farmer.get('Location'),
        "Date Ready": str(st.session_state.parsed_farmer.get('Date Ready')),
        "Time Ready": str(st.session_state.parsed_farmer.get('Time Ready'))
    })

    with open('farmer_data.json', 'w') as f:
        json.dump(all_farmers, f, indent=4)

    st.success("Farmer data saved successfully!")
