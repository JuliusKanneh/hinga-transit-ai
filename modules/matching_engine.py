def match_farmer_driver(farmer, driver):
    # --- Capacity check ---
    try:
        quantity = int(farmer['Quantity'])
    except:
        quantity = 0

    try:
        capacity = int(driver['Capacity (kg)'])
    except:
        capacity = 0

    capacity_ok = quantity <= capacity

    # --- Location check ---
    location_match = farmer['Location'].lower() in (driver['Origin'].lower() + " " + driver['Destination'].lower())

    # --- Crop preference check ---
    crop_match = farmer['Crop'].lower() in driver['Preferred Crop'].lower() or driver['Preferred Crop'] == "Any"

    # --- Date match ---
    date_match = str(farmer['Date Ready']) == str(driver['Date Available'])

    # --- Time match (basic for now: must be exactly same hour) ---
    farmer_time = str(farmer.get('Time Ready'))
    driver_time = str(driver.get('Time Available'))
    time_match = farmer_time == driver_time or farmer_time in driver_time or driver_time in farmer_time

    # --- Urgency (optional for MVP) ---
    urgency_ok = True  # You can later add logic for urgency prioritization

    # --- Final decision ---
    return capacity_ok and location_match and crop_match and date_match and time_match and urgency_ok