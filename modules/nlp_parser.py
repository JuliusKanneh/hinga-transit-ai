import re

def parse_driver_message(message):
    # Example crops
    crops = ['tomatoes', 'onions', 'potatoes', 'cabbage', 'maize']

    # Extract capacity (looks for numbers + kg or tons)
    capacity_match = re.search(r'(\d+)\s*(kg|tons)?', message.lower())
    capacity = capacity_match.group(1) if capacity_match else "Unknown"

    # Find crop preferences
    preferred_crop = "Any"
    for crop in crops:
        if crop in message.lower():
            preferred_crop = crop
            break

    # Extract route keywords (expandable)
    locations = ['musanze', 'kigali', 'nyanza', 'rubavu']
    origin = "Unknown"
    destination = "Unknown"

    # Look for patterns like "from X to Y"
    route_match = re.search(r'from\s+(\w+)\s+to\s+(\w+)', message.lower())
    if route_match:
        origin = route_match.group(1)
        destination = route_match.group(2)
    else:
        # Try to find just one location if "from...to..." pattern is missing
        for location in locations:
            if location in message.lower():
                if origin == "Unknown":
                    origin = location
                else:
                    destination = location

    # Available date or urgency (simplified for now)
    urgency = "Normal"
    if "urgent" in message.lower() or "asap" in message.lower():
        urgency = "High"

    return {
        "Capacity (kg)": capacity,
        "Preferred Crop": preferred_crop,
        "Origin": origin,
        "Destination": destination,
        "Urgency": urgency
    }

import re
import datetime
import dateparser

def parse_farmer_message(message):
    crops = ['tomatoes', 'onions', 'potatoes', 'cabbage', 'maize']

    # Extract quantity
    quantity_match = re.search(r'(\d+)\s*(kg|sacks|bags)?', message.lower())
    quantity = quantity_match.group(1) if quantity_match else "Unknown"

    # Find crop type
    crop_found = "Unknown"
    for crop in crops:
        if crop in message.lower():
            crop_found = crop
            break

    # Urgency
    urgency = "Normal"
    if "urgent" in message.lower() or "asap" in message.lower():
        urgency = "High"
    elif "next week" in message.lower():
        urgency = "Low"

    # Location
    locations = ['musanze', 'kigali', 'nyanza', 'rubavu']
    location_found = "Unknown"
    for location in locations:
        if location in message.lower():
            location_found = location
            break

    # FULL DATE PARSING 🔥
    date_found = dateparser.parse(message, settings={'PREFER_DATES_FROM': 'future'})
    if date_found:
        date_ready = date_found.date()  # Get just the date
    else:
        date_ready = None

    return {
        "Crop": crop_found,
        "Quantity": quantity,
        "Urgency": urgency,
        "Location": location_found,
        "Date Ready": date_ready
    }
