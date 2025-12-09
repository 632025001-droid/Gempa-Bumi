# ============================================
# 🌋 EARTHQUAKE PREDICTOR - SUPER SIMPLE
# ============================================

import streamlit as st
import datetime

st.set_page_config(page_title="Earthquake AI", layout="wide")

st.title("🌋 EARTHQUAKE IMPACT PREDICTOR")
st.markdown("### Mini AI Project")

# Sidebar
with st.sidebar:
    st.header("📊 Parameters")
    
    magnitude = st.slider("Magnitude", 3.0, 9.0, 6.5, 0.1)
    depth = st.slider("Depth (km)", 1.0, 700.0, 50.0, 1.0)
    
    st.info(f"Current: {magnitude:.1f} M at {depth:.0f} km")

# Prediction logic
if st.button("🎯 Predict Impact", type="primary"):
    # Simple prediction
    if magnitude < 4.0:
        impact = "Minor"
        color = "green"
    elif magnitude < 5.0:
        impact = "Light"
        color = "lightgreen"
    elif magnitude < 6.0:
        impact = "Moderate"
        color = "yellow"
    elif magnitude < 7.0:
        impact = "Strong"
        color = "orange"
    elif magnitude < 8.0:
        impact = "Major"
        color = "red"
    else:
        impact = "Severe"
        color = "darkred"
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Impact Level", impact)
    
    with col2:
        tsunami = "High" if magnitude > 7.5 and depth < 50 else "Low"
        st.metric("Tsunami Risk", tsunami)
    
    with col3:
        shaking = magnitude / (depth**0.5) * 10
        st.metric("Shaking Intensity", f"{shaking:.2f}")
    
    # Recommendations
    st.markdown("---")
    st.subheader("🚨 Recommendations")
    
    if impact in ["Major", "Severe"]:
        st.error("Evacuate immediately to higher ground!")
    elif impact in ["Strong", "Moderate"]:
        st.warning("Take cover under sturdy furniture")
    else:
        st.success("Stay alert for aftershocks")

# Footer
st.markdown("---")
st.markdown("**Components:** Data Input → Database → ML Analysis → Dashboard")
st.markdown(f"*Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*")
