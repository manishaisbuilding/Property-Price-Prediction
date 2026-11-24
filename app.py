import streamlit as st
import pandas as pd
import joblib

# Load trained model
model_data = joblib.load("best_house_model.pkl")

model = model_data["model"]
model_name = model_data["model_name"]
feature_columns = model_data["feature_columns"]
median_bedrooms = model_data["median_bedrooms"]
ocean_categories = model_data["ocean_categories"]

# Page Configuration
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# Application Title
st.title("🏠 California House Price Prediction")
st.write("Enter house details to predict the estimated house price.")

st.info(f"Selected Machine Learning Model: {model_name}")

# Input Form
st.subheader("Enter Property Details")

col1, col2 = st.columns(2)

with col1:
    longitude = st.number_input(
        "Longitude", value=-122.23, format="%.4f"
    )
    latitude = st.number_input(
        "Latitude", value=37.88, format="%.4f"
    )
    housing_median_age = st.number_input(
        "Housing Median Age", min_value=1, value=20
    )
    total_rooms = st.number_input(
        "Total Rooms", min_value=1, value=2000
    )
    total_bedrooms = st.number_input(
        "Total Bedrooms", min_value=1,
        value=int(median_bedrooms)
    )

with col2:
    population = st.number_input(
        "Population", min_value=1, value=1000
    )
    households = st.number_input(
        "Households", min_value=1, value=300
    )
    median_income = st.number_input(
        "Median Income", min_value=0.1, value=3.5
    )
    ocean_proximity = st.selectbox(
        "Ocean Proximity", ocean_categories
    )

# Prediction Button
if st.button("Predict House Price", type="primary"):

    input_data = {
        "longitude": longitude,
        "latitude": latitude,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income
    }

    # Create input with the same features used during training
    for column in feature_columns:
        if column.startswith("ocean_proximity_"):
            category = column.replace("ocean_proximity_", "")
            input_data[column] = int(
                ocean_proximity == category
            )

    input_df = pd.DataFrame([input_data])
    input_df = input_df.reindex(
        columns=feature_columns, fill_value=0
    )

    prediction = model.predict(input_df)[0]

    st.success("House Price Prediction Completed!")

    st.metric(
        label="Predicted Median House Value",
        value=f"${prediction:,.2f}"
    )

    st.caption(
        "This is an estimated prediction based on the trained model."
    )
