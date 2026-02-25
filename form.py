import streamlit as st
from camera_input_live import camera_input_live

# image = camera_input_live()

# if image:
#   st.image(image)

st.title("Streamlit tutorial")

st.chat_input("What are you asking today?")

st.chat_message("user",avatar="👌").write("Hello")

# st.balloons()