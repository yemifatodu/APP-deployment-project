import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.write("Select a page to explore or make predictions.")

page = st.sidebar.selectbox("Choose a Page", ("Predict", "Explore"))

# Page routing
if page == "Predict":
    st.title("Prediction Page")
    show_predict_page()
else:
    st.title("Exploration Page")
    show_explore_page()
