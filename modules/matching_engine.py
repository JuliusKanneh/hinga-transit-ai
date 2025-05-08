import pandas as pd

def match_farmer_driver(farmer_data, driver_data):
    # Check quantity vs. capacity
    try:
        quantity = int(farmer_data['Quantity'])
    except:
        quantity = 0

    try:
        capacity = int(driver_data['Capacity (kg)'])
    except:
        capacity = 0

    capacity_ok = quantity <= capacity

    # Check date availability
    date_match = (farmer_data['Urgency'] == "High") or (farmer_data['Date Ready'].strftime("%A") == driver_data['Available Date'])

    # Check route match (very basic for now)
    location_match = farmer_data['Location'].capitalize() in driver_data['Route']

    # Check crop match (optional, skip if unknown)
    crop_match = (farmer_data['Crop'].lower() in driver_data['Preferred Crop'].lower()) or driver_data['Preferred Crop'] == "Unknown"

    # Final decision
    if capacity_ok and date_match and location_match and crop_match:
        return True
    else:
        return False

farmer_data = {
    "Crop": "tomatoes",
    "Quantity": "300",
    "Urgency": "Normal",
    "Location": "Musanze",
    "Date Ready": pd.to_datetime("2024-05-09")  # Example date
}

driver_data = {
    "Capacity (kg)": "500",
    "Route": "Musanze to Kigali",
    "Preferred Crop": "tomatoes",
    "Available Date": "Thursday"
}

matched = match_farmer_driver(farmer_data, driver_data)
print("Match found?" , matched)
