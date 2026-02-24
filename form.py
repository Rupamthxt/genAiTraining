import streamlit as st
from camera_input_live import camera_input_live

image = camera_input_live()

if image:
  st.image(image)


st.title("Form Example")

st.chat_message("me", avatar="🦖").write("HI, this is me")
st.chat_message("you", avatar="👩‍🦰").write("HI, this is you")

st.chat_input(
    placeholder="Type your message here...",
    key="formInput"
              )

st.balloons()