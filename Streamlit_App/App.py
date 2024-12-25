import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns 
import warnings
warnings.filterwarnings("ignore")  

# Title of the app
st.title("Fitness Tracker System")

# Load the trained model
@st.cache
def load_model():
    with open('decision_tree_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# Sidebar for user inputs
st.sidebar.header("Input Parameters")

def user_inputs():
    age = st.sidebar.slider('Age', 18, 70, 30)
    weight = st.sidebar.slider('Weight (kg)', 40, 120, 70)
    height = st.sidebar.slider('Height (m)', 1.4, 2.1, 1.7)
    max_bpm = st.sidebar.slider('Max BPM', 100, 200, 150)
    avg_bpm = st.sidebar.slider('Avg BPM', 80, 180, 120)
    session_duration = st.sidebar.slider('Session Duration (hours)', 0.5, 3.0, 1.0)
    workout_frequency = st.sidebar.slider('Workout Frequency (days/week)', 1, 7, 3)
    water_intake = st.sidebar.slider('Water Intake (liters)', 0.5, 5.0, 2.0)
    fat_percentage = st.sidebar.slider('Fat Percentage', 5, 40, 20)

    # Create input data frame
    data = {
        'Age': age,
        'Weight (kg)': weight,
        'Height (m)': height,
        'Max_BPM': max_bpm,
        'Avg_BPM': avg_bpm,
        'Session_Duration (hours)': session_duration,
        'Workout_Frequency (days/week)': workout_frequency,
        'Water_Intake (liters)': water_intake,
        'Fat_Percentage': fat_percentage
    }
    return pd.DataFrame(data, index=[0])

inputs = user_inputs()

# Display user inputs
st.subheader("User Input Parameters")
st.write(inputs)

# Calculate BMI
inputs['BMI'] = inputs['Weight (kg)'] / (inputs['Height (m)'] ** 2)

# Predict calories burned
prediction = model.predict(inputs)

# Display the prediction
st.subheader("Prediction")
st.write(f"Estimated Calories Burned: {prediction[0]:.2f}")

# Visualization: Correlation Heatmap
if st.button("Show Correlation Heatmap"):
    st.subheader("Correlation Heatmap of Dataset")
    data = pd.read_csv('Gym_data.csv')  # Load your dataset
    correlation_matrix = data.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    st.pyplot(plt)

# Visualization: Scatter Plot
if st.button("Show Scatter Plot"):
    st.subheader("Scatter Plot: Session Duration vs. Calories Burned")
    data = pd.read_csv('Gym_data.csv')
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=data['Session_Duration (hours)'], y=data['Calories_Burned'])
    st.pyplot(plt)
