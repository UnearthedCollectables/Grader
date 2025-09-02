import streamlit as st
from grader.logic import evaluate_card

st.title("AI Card Grader")

grading_style = st.radio("Select Grading Style:", ["ACE", "PSA"])

uploaded_front = st.file_uploader("Upload front image", type=["jpg","jpeg","png"])
uploaded_back = st.file_uploader("Upload back image", type=["jpg","jpeg","png"])

if uploaded_front and uploaded_back:
    result = evaluate_card(uploaded_front, uploaded_back, grading_style)
    
    # Check for detection errors
    if result[0] is None:
        st.warning(result[1]["Error"])
    else:
        overall_grade, sub_grades = result
        st.success(f"Overall {grading_style} Grade: {overall_grade}")
        st.write("### Sub-Grades")
        for category, score in sub_grades.items():
            st.write(f"{category}: {score}")
