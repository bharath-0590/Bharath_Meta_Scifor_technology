import streamlit as st  # type: ignore

'''
# Title

st.title("Streamlit App")

# Text input

name = st.text_input("Enter name:")

# Slider input for age

age = st.slider("Select your age:", 20, 25)

# Display a message

st.write(f"Hello, {name}! You are {age} years old.")

# Button

if st.button("Submit"):
    st.write(f"Thank you for submitting your information!")
    st.balloons()  # Show balloons when button is clicked
    st.stop()  # Stop the app after button is clicked

'''
# Define a simple user authentication function
def authenticate(username, password):
    # Hardcoded credentials (you can modify or expand this logic)
    if username == "admin" and password == "password123":
        return True
    else:
        return False

# Create the login form using Streamlit
def login_form():
    # Display the login form title
    st.title("Login Form")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")  # Hide password input

    # Create a login button
    login_button = st.button("Login")

    # Process login if button is clicked
    if login_button:
        if authenticate(username, password):
            st.success(f"Welcome, {username}!")  # Display a success message
        else:
            st.error("Invalid username or password")  # Display an error message

# Run the login form
login_form()

    
     
