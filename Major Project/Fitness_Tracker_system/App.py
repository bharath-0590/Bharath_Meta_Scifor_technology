import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Title of the app
st.title("Fitness Tracker System")

# Description
st.write("""
This application predicts **Calories Burned** based on fitness and health metrics.
Upload the required parameters to get started.
""")

# Sidebar for user inputs
st.sidebar.header("Input Parameters")

# Function to get user inputs
def user_input_features():
    Age = st.sidebar.slider("Age", 10, 80, 25)
    Weight_kg = st.sidebar.slider("Weight (kg)", 30, 150, 70)
    Height_m = st.sidebar.slider("Height (m)", 1.0, 2.5, 1.7)
    Max_BPM = st.sidebar.slider("Max BPM", 100, 220, 160)
    Avg_BPM = st.sidebar.slider("Avg BPM", 60, 180, 120)
    Resting_BPM = st.sidebar.slider("Resting BPM", 40, 120, 70)
    Session_Duration = st.sidebar.slider("Session Duration (hours)", 0.5, 5.0, 1.0)
    Fat_Percentage = st.sidebar.slider("Fat Percentage", 5, 50, 20)
    Water_Intake = st.sidebar.slider("Water Intake (liters)", 0.5, 5.0, 2.0)
    Workout_Frequency = st.sidebar.slider("Workout Frequency (days/week)", 1, 7, 3)
    BMI = Weight_kg / (Height_m ** 2)
    
    data = {
        "Age": Age,
        "Weight (kg)": Weight_kg,
        "Height (m)": Height_m,
        "Max_BPM": Max_BPM,
        "Avg_BPM": Avg_BPM,
        "Resting_BPM": Resting_BPM,
        "Session_Duration (hours)": Session_Duration,
        "Fat_Percentage": Fat_Percentage,
        "Water_Intake (liters)": Water_Intake,
        "Workout_Frequency (days/week)": Workout_Frequency,
        "BMI": BMI
    }
    features = pd.DataFrame(data, index=[0])
    return features

# Get user input
input_df = user_input_features()

# Display input
st.subheader("User Input Parameters")
st.write(input_df)

# Load the saved model
model_file = 'decision_tree_model.pkl'  # Update the path if necessary
with open(model_file, 'rb') as file:
    model = pickle.load(file)

# Make predictions
prediction = model.predict(input_df)

# Display results
st.subheader("Prediction")
st.write(f"Predicted Calories Burned: {prediction[0]:.2f}")
