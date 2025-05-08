import streamlit as st
import pandas as pd
import os

st.title("AgriRoute AI - Crop Transport Matching")

st.sidebar.title("AgriRoute AI")
st.sidebar.write("Smart transport matching for farmers and drivers")

# Save Farmer and Driver Data
def save_farmer_data(data, filename):
    filename = filename + ".csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = df.append(data, ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_csv(filename, index=False)

# Farmer Input Form
st.header("Farmer Input")

with st.form("farmer_form"):
    farmer_name = st.text_input("Farmer Name")
    crop_type = st.text_input("Crop Type (e.g., Tomatoes, Potatoes)")
    quantity = st.number_input("Quantity (kg)", min_value=1)
    location = st.text_input("Pickup Location")
    date_ready = st.date_input("Date Ready for Pickup")
    urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High"])
    submitted_farmer = st.form_submit_button("Submit Farmer Request")

    if submitted_farmer:
        farmer_data = {
            "Name": farmer_name,
            "Crop Type": crop_type,
            "Quantity (kg)": quantity,
            "Location": location,
            "Date Ready": date_ready,
            "Urgency": urgency
            }
        save_farmer_data(farmer_data, "farmer_data")
        st.success("Farmer request submitted and saved!")

# Driver Input Form
st.header("Driver Input")

with st.form("driver_form"):
    driver_name = st.text_input("Driver Name")
    vehicle_capacity = st.number_input("Vehicle Capacity (kg)", min_value=50)
    preferred_crop = st.text_input("Preferred Crop Type(s)")
    route = st.text_input("Route (e.g., Musanze to Kigali)")
    date_available = st.date_input("Available Date")
    submitted_driver = st.form_submit_button("Submit Driver Availability")

    if submitted_driver:
        driver_data = {
            "Name": driver_name,
            "Vehicle Capacity (kg)": vehicle_capacity,
            "Preferred Crops": preferred_crop,
            "Route": route,
            "Available Date": date_available
        }
        save_farmer_data(driver_data, "driver_data")
        st.success("Driver request submitted and saved!")