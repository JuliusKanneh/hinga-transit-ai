import re
import dateparser

# ------------- Farmer Message Parsing -------------
def parse_driver_message(message):
    crops = ['tomatoes', 'onions', 'potatoes', 'cabbage', 'maize']

    # Extract capacity
    capacity_match = re.search(r'(\d+)\s*(kg|tons)?', message.lower())
    capacity = capacity_match.group(1) if capacity_match else "Unknown"

    # Preferred crop
    preferred_crop = "Any"
    for crop in crops:
        if crop in message.lower():
            preferred_crop = crop
            break

    # Route
    locations = ['musanze', 'kigali', 'nyanza', 'rubavu']
    origin = "Unknown"
    destination = "Unknown"
    route_match = re.search(r'from\s+(\w+)\s+to\s+(\w+)', message.lower())
    if route_match:
        origin = route_match.group(1)
        destination = route_match.group(2)
    else:
        for location in locations:
            if origin == "Unknown" and location in message.lower():
                origin = location
            elif destination == "Unknown" and location in message.lower():
                destination = location

    # Urgency
    urgency = "Normal"
    if "urgent" in message.lower() or "asap" in message.lower():
        urgency = "High"

    # FULL DATE & TIME PARSING
    date_found = dateparser.parse(message, settings={'PREFER_DATES_FROM': 'future'})
    if date_found:
        date_available = date_found.date()
        time_available = date_found.time()
    else:
        date_available = None
        time_available = None

    return {
        "Capacity (kg)": capacity,
        "Preferred Crop": preferred_crop,
        "Origin": origin,
        "Destination": destination,
        "Urgency": urgency,
        "Date Available": date_available,
        "Time Available": time_available
    }

# ------------- Farmer Message Parsing -------------
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
