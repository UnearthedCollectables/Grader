
import streamlit as st
from grader.logic import evaluate_card

st.title("AI Card Grader (Demo)")

uploaded_front = st.file_uploader("Upload front image", type=["jpg", "jpeg", "png"])
uploaded_back = st.file_uploader("Upload back image", type=["jpg", "jpeg", "png"])

if uploaded_front and uploaded_back:
    grade = evaluate_card(uploaded_front, uploaded_back)
    st.success(f"Predicted Grade: {grade}")
