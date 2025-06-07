# app.py

import streamlit as st
import joblib
import numpy as np

# Load model and feature columns
model = joblib.load('car_price_model.pkl')
feature_columns = joblib.load('model_features.pkl')

st.title("Car Price Prediction App 🚗")

# Collect user input
km_driven = st.number_input("Kilometers Driven", value=50000)
mileage = st.number_input("Mileage (kmpl)", value=20.0)
engine = st.number_input("Engine (CC)", value=1200)
max_power = st.number_input("Max Power (bhp)", value=75.0)
seats = st.selectbox("Seats", [2, 4, 5, 6, 7])
car_age = st.slider("Car Age (Years)", 0, 30, 5)

fuel = st.selectbox("Fuel Type", ["Diesel", "LPG", "Petrol"])
seller_type = st.selectbox("Seller Type", ["Individual", "Trustmark Dealer"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
owner = st.selectbox("Owner", [
    "First Owner", "Second Owner", "Third Owner",
    "Fourth & Above Owner", "Test Drive Car"
])

# Prepare input data
input_data = np.zeros(len(feature_columns))
input_data[0:6] = [km_driven, mileage, engine, max_power, seats, car_age]

# Manual encoding
if fuel == "Diesel":
    input_data[feature_columns.index("fuel_Diesel")] = 1
elif fuel == "LPG":
    input_data[feature_columns.index("fuel_LPG")] = 1
elif fuel == "Petrol":
    input_data[feature_columns.index("fuel_Petrol")] = 1

if seller_type == "Individual":
    input_data[feature_columns.index("seller_type_Individual")] = 1
elif seller_type == "Trustmark Dealer":
    input_data[feature_columns.index("seller_type_Trustmark Dealer")] = 1

if transmission == "Manual":
    input_data[feature_columns.index("transmission_Manual")] = 1

owner_map = {
    "Second Owner": "owner_Second Owner",
    "Third Owner": "owner_Third Owner",
    "Fourth & Above Owner": "owner_Fourth & Above Owner",
    "Test Drive Car": "owner_Test Drive Car"
}
if owner in owner_map:
    input_data[feature_columns.index(owner_map[owner])] = 1

# Predict
if st.button("Predict Selling Price"):
    predicted_price = model.predict([input_data])[0]
    st.success(f"Estimated Selling Price: ₹{int(predicted_price):,}")
