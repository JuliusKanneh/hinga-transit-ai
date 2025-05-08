import re
import streamlit as st

def parse_farmer_message(message):
    # Example crops (add more as needed)
    crops = ['tomatoes', 'onions', 'potatoes', 'cabbage', 'maize']

    # Extract quantity (looks for numbers + kg or sacks or bags)
    quantity_match = re.search(r'(\d+)\s*(kg|sacks|bags)?', message.lower())
    quantity = quantity_match.group(1) if quantity_match else "Unknown"

    # Find crop type
    crop_found = "Unknown"
    for crop in crops:
        if crop in message.lower():
            crop_found = crop
            break

    # Find urgency keywords
    urgency = "Normal"
    if "urgent" in message.lower() or "asap" in message.lower():
        urgency = "High"
    elif "next week" in message.lower():
        urgency = "Low"

    # Location extraction (this can be expanded later)
    locations = ['musanze', 'kigali', 'nyanza', 'rubavu']  # Example
    location_found = "Unknown"
    for location in locations:
        if location in message.lower():
            location_found = location
            break

    return {
        "Crop": crop_found,
        "Quantity": quantity,
        "Urgency": urgency,
        "Location": location_found
    }

# Example usage
msg = "I have 3 sacks of tomatoes ready by Thursday in Musanze."
# msg = "I have 3 sacks of tomatoes ready today in Musanze."
parsed = parse_farmer_message(msg)
print(parsed)

st.title("Farmer Message Parser")
st.header("Farmer Free Text Input")

farmer_message = st.text_area("Enter your message (e.g., 'I have 3 sacks of tomatoes ready by Thursday in Musanze.')")

if st.button("Parse Farmer Message"):
    parsed_data = parse_farmer_message(farmer_message)
    st.write("Parsed Data:")
    st.json(parsed_data)
