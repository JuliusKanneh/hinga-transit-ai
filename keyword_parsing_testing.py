import re
import streamlit as st
from modules.nlp_parser import parse_farmer_message
from modules.nlp_parser import parse_driver_message
from modules.matching_engine import match_farmer_driver

st.title("Message Parser Demo")

st.header("Farmer Free Text Input")
farmer_message = st.text_area("Enter your message (e.g., 'I have 3 sacks of tomatoes ready by Thursday in Musanze.')")

if st.button("Parse Farmer Message"):
    parsed_data = parse_farmer_message(farmer_message)
    st.write("Parsed Data:")
    st.json(parsed_data)

    if not parsed_data['Date Ready']:
        missing_date = st.text_input("We couldn't find a date in your message. Please enter the day the crops will be ready (e.g., May 10, Thursday, next week):")
        if missing_date:
            # Parse the manual input too
            manual_date = dateparser.parse(missing_date, settings={'PREFER_DATES_FROM': 'future'})
            if manual_date:
                parsed_data['Date Ready'] = manual_date.date()

    st.write("Final Farmer Data:")
    st.json(parsed_data)


st.header("Driver Free Text Input")
driver_message = st.text_area("Enter your message (e.g., 'Available for leafy crops. Can carry up to 500kg. From Musanze to Kigali. ASAP.')")

if st.button("Parse Driver Message"):
    parsed_data = parse_driver_message(driver_message)
    st.write("Parsed Data:")
    st.json(parsed_data)

# Test matching engine with parsed data
if st.button("Check Match"):
    # Parse both farmer and driver messages
    parsed_farmer = parse_farmer_message(farmer_message)
    parsed_driver = parse_driver_message(driver_message)

    # You’ll need to fake a 'Date Ready' in this case or grab from form
    parsed_farmer['Date Ready'] = parsed_data  # from your form input

    # Run matcher
    is_match = match_farmer_driver(parsed_farmer, parsed_driver)
    if is_match:
        st.success("MATCH FOUND ✅ : This driver can carry this farmer’s crops.")
    else:
        st.error("No match ❌ : This driver isn’t a good fit for this farmer’s crops.")
