import streamlit as st # type: ignore

# Streamlit form
st.title("Simple Registration Form")

# Form inputs
with st.form(key='registration_form'):
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    password = st.text_input("Enter your password:", type='password')
    
    # Submit button
    submit_button = st.form_submit_button(label='Submit')

# Show the details on submit
if submit_button:
    st.write(f"**Name:** {name}")
    st.write(f"**Email:** {email}")
    st.write("Registration Successful!")
