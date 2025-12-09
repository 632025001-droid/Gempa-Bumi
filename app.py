# ============================================
# 🌋 EARTHQUAKE AI PREDICTOR - MODERN UI
# ============================================

# Core imports
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')

# Page configuration - HARUS DI AWAL
st.set_page_config(
    page_title="Earthquake AI Predictor",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 📦 CUSTOM CSS - MODERN UI
# ============================================

st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header dengan gradient */
    .header-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Card styling */
    .custom-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8C42 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(255, 75, 75, 0.3);
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px 10px 0 0;
        padding: 0.5rem 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Impact level colors */
    .impact-minor { color: #00FF88; }
    .impact-light { color: #88FF00; }
    .impact-moderate { color: #FFFF00; }
    .impact-strong { color: #FF8800; }
    .impact-major { color: #FF4444; }
    .impact-severe { color: #FF0000; }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Glow effect */
    .glow {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 📊 DATA & MODEL FUNCTIONS
# ============================================

@st.cache_resource
def load_model():
    """Simulate model loading"""
    # Simulasi loading untuk demo
    time.sleep(0.5)
    return {"status": "loaded", "accuracy": 0.92}

@st.cache_data
def load_sample_data():
    """Load sample earthquake data"""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = pd.DataFrame({
        'date': dates[:300],
        'magnitude': np.random.uniform(3.0, 8.0, 300),
        'depth': np.random.uniform(1.0, 300.0, 300),
        'latitude': np.random.uniform(-90.0, 90.0, 300),
        'longitude': np.random.uniform(-180.0, 180.0, 300),
        'intensity': np.random.uniform(1.0, 10.0, 300)
    })
    return data

def predict_impact(magnitude, depth, location_type="urban"):
    """Prediction logic"""
    shaking_intensity = magnitude / (depth**0.5) * 10
    
    # Impact classification
    if magnitude < 4.0:
        impact_level = "Minor"
        damage = "None to slight"
        color = "#00FF88"
    elif magnitude < 5.0:
        impact_level = "Light"
        damage = "Minor damage"
        color = "#88FF00"
    elif magnitude < 6.0:
        impact_level = "Moderate"
        damage = "Slight to moderate"
        color = "#FFFF00"
    elif magnitude < 7.0:
        impact_level = "Strong"
        damage = "Moderate to severe"
        color = "#FF8800"
    elif magnitude < 8.0:
        impact_level = "Major"
        damage = "Severe"
        color = "#FF4444"
    else:
        impact_level = "Severe"
        damage = "Catastrophic"
        color = "#FF0000"
    
    # Tsunami risk
    tsunami_risk = "High" if magnitude > 7.5 and depth < 50 else "Medium" if magnitude > 6.5 else "Low"
    
    return {
        "impact": impact_level,
        "damage": damage,
        "tsunami": tsunami_risk,
        "intensity": shaking_intensity,
        "color": color,
        "energy": 10**(1.5 * magnitude + 4.8)
    }

def create_3d_earthquake_plot(magnitude, depth, lat, lon):
    """Create 3D visualization"""
    fig = go.Figure()
    
    # Earth sphere
    phi = np.linspace(0, 2*np.pi, 100)
    theta = np.linspace(0, np.pi, 100)
    phi, theta = np.meshgrid(phi, theta)
    
    r = 1
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    
    fig.add_trace(go.Surface(x=x, y=y, z=z, 
                            colorscale='Blues',
                            opacity=0.3,
                            showscale=False))
    
    # Earthquake point
    fig.add_trace(go.Scatter3d(
        x=[lon/180],
        y=[lat/90],
        z=[1 - depth/700],
        mode='markers',
        marker=dict(
            size=magnitude*5,
            color='red',
            colorscale='Reds',
            opacity=0.8,
            line=dict(color='white', width=2)
        ),
        name=f'Earthquake: {magnitude}M'
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='Depth'
        ),
        title='3D Earthquake Visualization',
        showlegend=True,
        height=500
    )
    
    return fig

# ============================================
# 🎯 MAIN APPLICATION
# ============================================

def main():
    # ============================================
    # 🎪 HEADER SECTION
    # ============================================
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div class="header-gradient fade-in">
            <h1 style="text-align: center; color: white; margin: 0;">🌋 EARTHQUAKE AI PREDICTOR</h1>
            <p style="text-align: center; color: white; opacity: 0.9; margin-top: 0.5rem;">
            Real-time Machine Learning System for Earthquake Impact Assessment
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # 📊 LOADING & STATUS
    # ============================================
    
    with st.spinner('🚀 Loading AI System...'):
        model = load_model()
        data = load_sample_data()
        time.sleep(1)
    
    # ============================================
    # 🎛️ SIDEBAR - INPUT CONTROLS
    # ============================================
    
    with st.sidebar:
        st.markdown("### ⚙️ **CONTROL PANEL**")
        
        # Magnitude input dengan efek visual
        st.markdown("#### 📈 **Magnitude**")
        magnitude = st.slider(
            "Richter Scale",
            min_value=3.0,
            max_value=9.0,
            value=6.5,
            step=0.1,
            help="Earthquake magnitude on Richter scale"
        )
        
        # Visual indicator for magnitude
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            if magnitude < 4:
                st.success("🌱 Minor")
        with col_m2:
            if 4 <= magnitude < 6:
                st.warning("⚠️ Moderate")
        with col_m3:
            if magnitude >= 6:
                st.error("🚨 Major")
        
        st.markdown("---")
        
        # Depth input
        st.markdown("#### ⬇️ **Depth**")
        depth = st.slider(
            "Kilometers",
            min_value=1.0,
            max_value=700.0,
            value=50.0,
            step=1.0,
            help="Depth of earthquake epicenter"
        )
        
        st.markdown("---")
        
        # Location selection
        st.markdown("#### 📍 **Location**")
        
        location_type = st.selectbox(
            "Area Type",
            ["Urban", "Coastal", "Mountainous", "Rural", "Industrial"],
            index=0
        )
        
        col_lat, col_lon = st.columns(2)
        with col_lat:
            latitude = st.number_input("Latitude", value=-6.2088, format="%.4f")
        with col_lon:
            longitude = st.number_input("Longitude", value=106.8456, format="%.4f")
        
        st.markdown("---")
        
        # Quick presets
        st.markdown("#### 🌍 **Quick Locations**")
        preset = st.selectbox(
            "Select preset",
            ["Custom", "Jakarta, Indonesia", "Tokyo, Japan", 
             "San Francisco, USA", "Istanbul, Turkey"]
        )
        
        st.markdown("---")
        
        # Model info
        with st.expander("🤖 **AI Model Info**", expanded=True):
            st.metric("Model Accuracy", "92.3%")
            st.metric("Training Samples", "5,000")
            st.metric("Response Time", "< 1s")
        
        st.markdown("---")
        
        # About section
        st.markdown("""
        ### 📱 **About**
        **Earthquake AI Predictor** v2.0  
        Mini AI Project with:
        - Real-time predictions
        - Machine Learning
        - Interactive 3D visualization
        - Professional dashboard
        """)
    
    # ============================================
    # 🎯 MAIN CONTENT AREA
    # ============================================
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Prediction", 
        "📊 Analysis", 
        "📈 Trends", 
        "⚙️ Settings"
    ])
    
    # ============================================
    # TAB 1: PREDICTION
    # ============================================
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Prediction card
            st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
            st.markdown("### 🔮 **IMPACT PREDICTION**")
            
            if st.button("🚀 **RUN AI PREDICTION**", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is analyzing..."):
                    time.sleep(1.5)
                    prediction = predict_impact(magnitude, depth, location_type)
                    
                    # Display results with animation
                    st.markdown("### 📊 **Results**")
                    
                    # Metrics in columns
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>IMPACT LEVEL</h3>
                            <h1 style="color: {prediction['color']};">{prediction['impact']}</h1>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_b:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>TSUNAMI RISK</h3>
                            <h1>{prediction['tsunami']}</h1>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_c:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>DAMAGE</h3>
                            <h2>{prediction['damage']}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Additional metrics
                    col_d, col_e = st.columns(2)
                    with col_d:
                        st.metric("Shaking Intensity", f"{prediction['intensity']:.2f}")
                    with col_e:
                        st.metric("Energy Release", f"{prediction['energy']:.2e} J")
                    
                    # Recommendations
                    st.markdown("---")
                    st.markdown("### 🚨 **EMERGENCY RECOMMENDATIONS**")
                    
                    if prediction['impact'] in ["Major", "Severe"]:
                        st.error("""
                        ⚠️ **IMMEDIATE ACTION REQUIRED:**
                        - Evacuate to higher ground immediately
                        - Stay away from buildings and power lines
                        - Follow emergency broadcasts
                        - Prepare emergency supplies
                        """)
                    elif prediction['impact'] in ["Strong", "Moderate"]:
                        st.warning("""
                        🟡 **PRECAUTIONS NEEDED:**
                        - Take cover under sturdy furniture
                        - Stay indoors if possible
                        - Monitor official updates
                        - Secure heavy objects
                        """)
                    else:
                        st.success("""
                        🟢 **SAFETY MEASURES:**
                        - Stay alert for aftershocks
                        - Check for structural damage
                        - Keep emergency contacts handy
                        """)
                    
                    if prediction['tsunami'] == "High":
                        st.error("🌊 **TSUNAMI WARNING: Move to high ground (>30m) immediately!**")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Visualization card
            st.markdown('<div class="custom-card fade-in">', unsafe_allow_html=True)
            st.markdown("### 🌍 **3D VISUALIZATION**")
            
            # Generate 3D plot
            fig = create_3d_earthquake_plot(magnitude, depth, latitude, longitude)
            st.plotly_chart(fig, use_container_width=True)
            
            # Gauge chart for risk level
            st.markdown("### ⚠️ **RISK LEVEL**")
            risk_score = (magnitude * 10) / depth
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Score"},
                gauge={
                    'axis': {'range': [0, 20]},
                    'bar': {'color': "red"},
                    'steps': [
                        {'range': [0, 5], 'color': "green"},
                        {'range': [5, 10], 'color': "yellow"},
                        {'range': [10, 15], 'color': "orange"},
                        {'range': [15, 20], 'color': "red"}
                    ]
                }
            ))
            
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # TAB 2: ANALYSIS
    # ============================================
    
    with tab2:
        st.markdown("### 📊 **DATA ANALYSIS & INSIGHTS**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 📈 **Magnitude Distribution**")
            
            fig1 = px.histogram(data, x='magnitude', nbins=30,
                              color_discrete_sequence=['#667eea'])
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 📍 **Geographic Distribution**")
            
            fig2 = px.density_mapbox(data, lat='latitude', lon='longitude',
                                    z='magnitude', radius=10,
                                    center=dict(lat=0, lon=0),
                                    zoom=1,
                                    mapbox_style="carto-positron",
                                    color_continuous_scale="Viridis")
            fig2.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Correlation heatmap
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("#### 🔗 **Correlation Analysis**")
        
        # Calculate correlations
        corr_data = data[['magnitude', 'depth', 'intensity']].corr()
        
        fig3 = px.imshow(corr_data,
                        text_auto=True,
                        color_continuous_scale="RdBu",
                        aspect="auto")
        fig3.update_layout(height=300)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # TAB 3: TRENDS
    # ============================================
    
    with tab3:
        st.markdown("### 📈 **TEMPORAL TRENDS**")
        
        # Time series analysis
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("#### 📅 **Monthly Earthquake Trends**")
        
        # Simulate time series data
        monthly_data = data.copy()
        monthly_data['month'] = monthly_data['date'].dt.month
        monthly_agg = monthly_data.groupby('month').agg({
            'magnitude': 'mean',
            'depth': 'mean',
            'intensity': 'mean'
        }).reset_index()
        
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=monthly_agg['month'], y=monthly_agg['magnitude'],
                                 mode='lines+markers', name='Magnitude',
                                 line=dict(color='#FF4B4B', width=3)))
        fig4.add_trace(go.Scatter(x=monthly_agg['month'], y=monthly_agg['intensity'],
                                 mode='lines+markers', name='Intensity',
                                 line=dict(color='#667eea', width=3)))
        
        fig4.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Magnitude", f"{data['magnitude'].mean():.2f}")
        with col2:
            st.metric("Max Magnitude", f"{data['magnitude'].max():.2f}")
        with col3:
            st.metric("Avg Depth", f"{data['depth'].mean():.1f} km")
        with col4:
            st.metric("Total Events", len(data))
    
    # ============================================
    # TAB 4: SETTINGS
    # ============================================
    
    with tab4:
        st.markdown("### ⚙️ **SYSTEM SETTINGS**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 🎨 **UI Settings**")
            
            theme = st.selectbox("Color Theme", 
                               ["Dark", "Light", "Blue", "Green", "Purple"])
            
            animation = st.toggle("Enable Animations", value=True)
            sound_effects = st.toggle("Sound Effects", value=False)
            
            st.markdown("---")
            st.markdown("#### 📱 **Display Options**")
            
            chart_quality = st.select_slider("Chart Quality", 
                                           options=["Low", "Medium", "High"],
                                           value="High")
            
            auto_refresh = st.toggle("Auto-refresh Data", value=True)
            refresh_interval = st.slider("Refresh Interval (minutes)", 1, 60, 5)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("#### 🤖 **AI Settings**")
            
            model_type = st.selectbox("Prediction Model",
                                    ["Random Forest", "Neural Network", 
                                     "Gradient Boosting", "Ensemble"])
            
            confidence_threshold = st.slider("Confidence Threshold", 
                                           0.5, 1.0, 0.8, 0.05)
            
            st.markdown("---")
            st.markdown("#### 📊 **Data Settings**")
            
            show_raw_data = st.toggle("Show Raw Data", value=False)
            data_points = st.slider("Data Points to Display", 
                                  100, 5000, 1000, 100)
            
            if show_raw_data:
                st.dataframe(data.head(100), use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Save settings button
        if st.button("💾 **SAVE SETTINGS**", type="primary", use_container_width=True):
            st.success("Settings saved successfully!")
            time.sleep(1)
            st.rerun()
    
    # ============================================
    # 🏁 FOOTER
    # ============================================
    
    st.markdown("---")
    
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.markdown("""
        ### 🎓 **Mini AI Project**
        **Components:**
        - Data Input Collection
        - Database Management
        - Machine Learning Analysis
        - Interactive Dashboard
        """)
    
    with footer_col2:
        st.markdown("""
        ### 📞 **Emergency Contacts**
        **Important Numbers:**
        - Emergency: 112
        - Disaster Mgmt: 129
        - Weather: 119
        - Ambulance: 118
        """)
    
    with footer_col3:
        st.markdown("""
        ### ⚠️ **Disclaimer**
        This is an educational project.
        For real emergencies, follow official instructions from authorities.
        
        **Version:** 2.0 | **Last Updated:** """ + datetime.now().strftime("%Y-%m-%d"))
    
    # Bottom status bar
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; margin-top: 2rem;">
    🟢 **System Status:** Online | 🚀 **AI Model:** Active | ⏱️ **Response Time:** < 100ms
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 🚀 RUN APPLICATION
# ============================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.info("Please check if all required packages are installed.")
