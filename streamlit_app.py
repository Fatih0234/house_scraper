import streamlit as st
import pickle
import pandas as pd
from explore_page import show_explore_page
from predict_page import show_predict_page


# Sidebar choice
choice = st.sidebar.selectbox("Select Mode", ("Prediction", "Exploration"))

if choice == "Prediction":
    show_predict_page()
elif choice == "Exploration":
    show_explore_page()


