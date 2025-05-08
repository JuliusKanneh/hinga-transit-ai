import streamlit as st
import pandas as pd
import os

st.title("AgriRoute AI - Crop Transport Matching")

st.sidebar.title("AgriRoute AI")
st.sidebar.write("Smart transport matching for farmers and drivers")

# Save Farmer and Driver Data
def save_prompt(data, filename):
    filename = filename + ".csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = df.append(data, ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_csv(filename, index=False)

# Farmer Input Form
st.header("Type Prompt")

with st.form("prompt_form"):
    prompt = st.text_area("Enter your prompt here:", height=200)
    farmer_name = st.text_input("Farmer Name")
    submitted_farmer = st.form_submit_button("Submit Request")

    if submitted_farmer:
        prompt_data = {
            "Prompt": prompt,
            "Name": farmer_name,
            "Date": pd.Timestamp.now()
        }
        save_prompt(prompt_data, "prompt_data")
        st.success("Prompt submitted and saved!")