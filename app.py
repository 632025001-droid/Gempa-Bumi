import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Earthquake AI", layout="wide")

st.title("🌍 Earthquake Prediction System")

# Input
mag = st.slider("Magnitude", 3.0, 9.0, 6.0)
depth = st.slider("Depth (km)", 1.0, 700.0, 50.0)

# Simple prediction
if st.button("Predict"):
    shaking = mag / (depth**0.5) * 10
    
    if mag < 4: impact = "Minor"
    elif mag < 6: impact = "Moderate"
    elif mag < 7.5: impact = "Strong"
    else: impact = "Severe"
    
    st.success(f"Impact: {impact}")
    st.info(f"Shaking Intensity: {shaking:.2f}")
