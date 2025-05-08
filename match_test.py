import json
from modules import matching_engine as me
import streamlit as st

# Load the farmer and driver data from JSON files
with open('farmer_data.json', 'r') as f:
    farmers = json.load(f)

with open('driver_data.json', 'r') as f:
    drivers = json.load(f)

# Build the matching Loop
matches = []

for farmer in farmers:
    for driver in drivers:
        if me.match_farmer_driver(farmer, driver):
            matches.append({
                'Farmer': farmer,
                'Driver': driver
            })

st.header("Matching Results")

if matches:
    for idx, pair in enumerate(matches):
        st.subheader(f"Match {idx + 1}")
        st.write("Farmer Info:")
        st.json(pair['Farmer'])
        st.write("Driver Info:")
        st.json(pair['Driver'])
else:
    st.warning("No matches found yet.")
