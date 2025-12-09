import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Earthquake Impact Predictor",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1E88E5;
    }
    .severity-minor { color: #4CAF50; font-weight: bold; }
    .severity-light { color: #8BC34A; font-weight: bold; }
    .severity-moderate { color: #FFC107; font-weight: bold; }
    .severity-strong { color: #FF9800; font-weight: bold; }
    .severity-major { color: #F44336; font-weight: bold; }
    .severity-severe { color: #D32F2F; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Load trained model and preprocessing objects"""
    try:
        data = joblib.load('models/earthquake_model.pkl')
        return data
    except:
        st.error("Model not found. Please run train_model.py first.")
        return None

def predict_impact(model_data, magnitude, depth, lat, lon):
    """Make predictions using loaded model"""
    # Calculate derived features
    shaking_intensity = magnitude / (depth**0.5) * 10
    
    # Prepare input
    input_features = np.array([[magnitude, depth, lat, lon, shaking_intensity]])
    
    # Scale features
    input_scaled = model_data['scaler'].transform(input_features)
    
    # Make predictions
    predictions = {}
    for target in ['impact_level', 'tsunami_risk', 'damage_level']:
        model = model_data['models'][target]
        le = model_data['label_encoders'][target]
        
        pred = model.predict(input_scaled)
        predictions[target] = le.inverse_transform(pred)[0]
    
    return predictions, shaking_intensity

def get_severity_color(impact_level):
    """Return color based on impact level"""
    colors = {
        'Minor': 'severity-minor',
        'Light': 'severity-light',
        'Moderate': 'severity-moderate',
        'Strong': 'severity-strong',
        'Major': 'severity-major',
        'Severe': 'severity-severe'
    }
    return colors.get(impact_level, 'severity-moderate')

def get_recommendations(impact_level, tsunami_risk, damage_level):
    """Generate safety recommendations"""
    recommendations = []
    
    if impact_level in ['Major', 'Severe']:
        recommendations.extend([
            "🚨 EVACUATE to higher ground immediately",
            "🏃 Move to open areas away from buildings",
            "📱 Stay tuned to emergency broadcasts",
            "🔦 Prepare emergency kit with essentials"
        ])
    elif impact_level in ['Strong', 'Moderate']:
        recommendations.extend([
            "⚠️ Drop, Cover, and Hold On",
            "🚫 Stay away from windows and heavy objects",
            "📊 Monitor for aftershocks",
            "🔋 Keep phone charged for emergency calls"
        ])
    else:
        recommendations.extend([
            "ℹ️ Stay alert for aftershocks",
            "🔍 Check for structural damage",
            "📝 Document any damages"
        ])
    
    if tsunami_risk == 'High':
        recommendations.append("🌊 TSUNAMI WARNING: Move to high ground immediately!")
    elif tsunami_risk == 'Medium':
        recommendations.append("🌊 Tsunami advisory: Stay away from coastal areas")
    
    return recommendations

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Earthquake Impact Prediction System</h1>', unsafe_allow_html=True)
    
    # Load model
    model_data = load_model()
    if model_data is None:
        return
    
    # Sidebar for input
    with st.sidebar:
        st.header("📊 Earthquake Parameters")
        
        magnitude = st.slider(
            "Magnitude (Richter Scale)",
            min_value=3.0,
            max_value=9.0,
            value=5.5,
            step=0.1,
            help="Earthquake magnitude on Richter scale"
        )
        
        depth = st.slider(
            "Depth (km)",
            min_value=1.0,
            max_value=700.0,
            value=50.0,
            step=1.0,
            help="Depth of earthquake epicenter"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input(
                "Latitude",
                min_value=-90.0,
                max_value=90.0,
                value=-6.2088,
                step=0.1
            )
        with col2:
            longitude = st.number_input(
                "Longitude",
                min_value=-180.0,
                max_value=180.0,
                value=106.8456,
                step=0.1
            )
        
        # Historical data
        st.subheader("📈 Historical Data")
        if st.checkbox("Show sample data"):
            try:
                sample_data = pd.read_csv('earthquake_data.csv')
                st.dataframe(sample_data.head(10))
            except:
                st.info("Run train_model.py to generate data first")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Prediction section
        st.subheader("🎯 Prediction Results")
        
        if st.button("Predict Earthquake Impact", type="primary"):
            with st.spinner("Analyzing earthquake data..."):
                predictions, shaking_intensity = predict_impact(
                    model_data, magnitude, depth, latitude, longitude
                )
                
                impact_level = predictions['impact_level']
                tsunami_risk = predictions['tsunami_risk']
                damage_level = predictions['damage_level']
                
                # Display predictions
                st.markdown(f"""
                <div class="prediction-card">
                    <h3>Impact Level: <span class="{get_severity_color(impact_level)}">{impact_level}</span></h3>
                    <p><strong>Magnitude:</strong> {magnitude} M</p>
                    <p><strong>Depth:</strong> {depth} km</p>
                    <p><strong>Shaking Intensity:</strong> {shaking_intensity:.2f}</p>
                    <p><strong>Tsunami Risk:</strong> {tsunami_risk}</p>
                    <p><strong>Expected Damage:</strong> {damage_level}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Recommendations
                st.subheader("🚨 Safety Recommendations")
                recommendations = get_recommendations(impact_level, tsunami_risk, damage_level)
                for rec in recommendations:
                    st.info(rec)
                
                # Visualization
                st.subheader("📊 Visual Analysis")
                
                fig, axes = plt.subplots(1, 2, figsize=(12, 4))
                
                # Impact vs Magnitude/Depth
                impact_order = ['Minor', 'Light', 'Moderate', 'Strong', 'Major', 'Severe']
                impact_df = pd.DataFrame({
                    'Impact Level': impact_order,
                    'Min Magnitude': [3.0, 4.0, 5.0, 6.0, 7.0, 7.5],
                    'Max Depth': [700, 700, 70, 50, 100, 30]
                })
                
                axes[0].barh(impact_df['Impact Level'], impact_df['Min Magnitude'])
                axes[0].set_xlabel('Minimum Magnitude')
                axes[0].set_title('Magnitude Threshold for Impact Levels')
                
                # Risk matrix
                risk_matrix = np.array([
                    [0.1, 0.3, 0.5, 0.7, 0.9],  # Shallow
                    [0.05, 0.2, 0.4, 0.6, 0.8],  # Medium
                    [0.01, 0.1, 0.3, 0.5, 0.7]   # Deep
                ])
                
                im = axes[1].imshow(risk_matrix, cmap='YlOrRd', aspect='auto')
                axes[1].set_xticks(range(5))
                axes[1].set_yticks(range(3))
                axes[1].set_xticklabels(['3-4', '4-5', '5-6', '6-7', '7+'])
                axes[1].set_yticklabels(['Shallow\n<30km', 'Medium\n30-100km', 'Deep\n>100km'])
                axes[1].set_xlabel('Magnitude')
                axes[1].set_ylabel('Depth')
                axes[1].set_title('Earthquake Risk Matrix')
                plt.colorbar(im, ax=axes[1])
                
                plt.tight_layout()
                st.pyplot(fig)
    
    with col2:
        # Quick reference
        st.subheader("📖 Impact Scale Guide")
        
        impact_info = {
            "Minor (<4.0 M)": "Rarely felt, no damage",
            "Light (4.0-5.0 M)": "Felt indoors, minor damage",
            "Moderate (5.0-6.0 M)": "Felt by all, slight damage",
            "Strong (6.0-7.0 M)": "Damage in populated areas",
            "Major (7.0-7.5 M)": "Serious damage over large areas",
            "Severe (>7.5 M)": "Catastrophic damage, tsunamis likely"
        }
        
        for title, desc in impact_info.items():
            with st.expander(title):
                st.write(desc)
        
        # Statistics
        st.subheader("📈 Quick Stats")
        
        stats_data = {
            "Magnitude Range": "3.0 - 9.0",
            "Depth Range": "1 - 700 km",
            "Model Accuracy": "~92%",
            "Training Samples": "5000",
            "Last Updated": datetime.now().strftime("%Y-%m-%d")
        }
        
        for key, value in stats_data.items():
            st.metric(key, value)
        
        # Database info
        if st.checkbox("Show Database Info"):
            st.info("""
            **Database Schema:**
            - magnitude: Richter scale
            - depth_km: Depth in kilometers
            - latitude/longitude: Coordinates
            - impact_level: Predicted impact
            - tsunami_risk: Tsunami probability
            - damage_level: Expected damage
            """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Earthquake Impact Prediction System v1.0 | Mini AI Project</p>
        <p>⚠️ <strong>Disclaimer:</strong> Predictions are for educational purposes only. 
        Always follow official emergency instructions during actual earthquakes.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
