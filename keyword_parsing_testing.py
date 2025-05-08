import streamlit as st
from modules.nlp_parser import parse_farmer_message
from modules.nlp_parser import parse_driver_message
from modules.matching_engine import match_farmer_driver
import dateparser

st.title("Message Parser Demo")

# ---------------------------- Farmer Input Form ----------------------------
st.header("Farmer Free Text Input")

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


# ---------------------------- Driver Input Form ----------------------------
st.header("Driver Free Text Input")
driver_message = st.text_area("Enter your message (e.g., 'Available for leafy crops. Can carry up to 500kg. From Musanze to Kigali. ASAP.')")

import json
import os

if 'parsed_driver' not in st.session_state:
    st.session_state.parsed_driver = {}

st.header("Driver Free Text Input")

driver_message = st.text_area(
    "Enter your message (e.g., 'Available for leafy crops. Can carry up to 500kg. From Musanze to Kigali. ASAP.')",
    key="driver_text"
)

if st.button("Parse Driver Message"):
    parsed_driver_data = parse_driver_message(driver_message)

    # Always add missing keys to avoid KeyError later
    if 'Time Available' not in parsed_driver_data:
        parsed_driver_data['Time Available'] = None

    st.session_state.parsed_driver = parsed_driver_data

    st.write("Parsed Data:")
    st.json(parsed_driver_data)

    # --- Check for missing Date Available ---
    if not parsed_driver_data['Date Available']:
        missing_date_driver = st.text_input(
            "We couldn't find the available date in your message. Please enter the date (e.g., May 10):",
            key="driver_date"
        )
        if missing_date_driver:
            manual_date_driver = dateparser.parse(
                missing_date_driver, settings={'PREFER_DATES_FROM': 'future'}
            )
            if manual_date_driver:
                st.session_state.parsed_driver['Date Available'] = manual_date_driver.date()
                if not st.session_state.parsed_driver.get('Time Available'):
                    st.session_state.parsed_driver['Time Available'] = manual_date_driver.time()

    # --- Check for missing Time Available ---
    if not st.session_state.parsed_driver.get('Time Available'):
        missing_time_driver = st.text_input(
            "Please specify the time you're available (e.g., 8:00 AM):",
            key="driver_time"
        )
        if missing_time_driver:
            manual_time_driver = dateparser.parse(missing_time_driver)
            if manual_time_driver:
                st.session_state.parsed_driver['Time Available'] = manual_time_driver.time()

    # --- REDISPLAY updated JSON ---
    st.write("Updated Driver Data after filling missing details:")
    st.json(st.session_state.parsed_driver)

    # --- Save to JSON ---
    if not os.path.exists('driver_data.json'):
        all_drivers = []
    else:
        with open('driver_data.json', 'r') as f:
            try:
                all_drivers = json.load(f)
            except json.JSONDecodeError:
                all_drivers = []

    all_drivers.append({
        "Capacity (kg)": st.session_state.parsed_driver.get('Capacity (kg)'),
        "Preferred Crop": st.session_state.parsed_driver.get('Preferred Crop'),
        "Origin": st.session_state.parsed_driver.get('Origin'),
        "Destination": st.session_state.parsed_driver.get('Destination'),
        "Urgency": st.session_state.parsed_driver.get('Urgency'),
        "Date Available": str(st.session_state.parsed_driver.get('Date Available')),
        "Time Available": str(st.session_state.parsed_driver.get('Time Available'))
    })

    with open('driver_data.json', 'w') as f:
        json.dump(all_drivers, f, indent=4)

    st.success("Driver data saved successfully!")

# ----------- Matching Section --------------
st.header("Match Farmer and Driver")

if st.button("Check Match"):
    if 'parsed_farmer' in st.session_state and 'parsed_driver' in st.session_state:
        parsed_farmer = st.session_state.parsed_farmer
        parsed_driver = st.session_state.parsed_driver

        is_match = match_farmer_driver(parsed_farmer, parsed_driver)
        if is_match:
            st.success("MATCH FOUND ✅ : This driver can carry this farmer’s crops.")
        else:
            st.error("No match ❌ : This driver isn’t a good fit for this farmer’s crops.")
    else:
        st.warning("Please parse both farmer and driver messages before matching.")
