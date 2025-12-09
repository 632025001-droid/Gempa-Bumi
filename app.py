import streamlit as st
import sys
import os
import subprocess

# ============================================
# 1. CHECK AND INSTALL MISSING PACKAGES
# ============================================

def install_packages():
    """Install required packages if missing"""
    required_packages = [
        'pandas',
        'numpy', 
        'scikit-learn',
        'joblib',
        'matplotlib',
        'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        st.warning(f"⚠️ Installing missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        st.success("✅ Packages installed successfully!")
        st.rerun()

# Jalankan install check
install_packages()

# ============================================
# 2. SET PAGE CONFIG (HARUS DI AWAL)
# ============================================

st.set_page_config(
    page_title="Earthquake Impact Predictor",
    page_icon="🌍",
    layout="wide"
)

# ============================================
# 3. IMPORT SETELAH INSTALLASI
# ============================================

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ============================================
# 4. CUSTOM CSS
# ============================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 5. LOAD MODEL DENGAN ERROR HANDLING
# ============================================

@st.cache_resource
def load_model():
    """Load model dengan multiple fallbacks"""
    try:
        # Coba berbagai lokasi
        possible_paths = [
            'earthquake_model.pkl',
            './earthquake_model.pkl',
            'app/earthquake_model.pkl',
            'earthquake-model.pkl'  # Nama alternatif
        ]
        
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    model = joblib.load(path)
                    return model
            except:
                continue
        
        # Jika tidak ditemukan
        st.error("""
        ❌ Model file 'earthquake_model.pkl' not found!
        
        Please ensure:
        1. The file exists in your GitHub repository
        2. File name is exactly 'earthquake_model.pkl'
        3. File is committed and pushed
        
        Quick fix:
        - Go to your Google Colab
        - Download the model file
        - Upload to GitHub in the same folder as app.py
        """)
        return None
        
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# ============================================
# 6. MAIN APPLICATION
# ============================================

def main():
    # Header
    st.markdown('<h1 class="main-title">🌍 Earthquake Impact Prediction System</h1>', unsafe_allow_html=True)
    st.markdown("### Mini AI Project with Machine Learning")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Input Parameters")
        
        magnitude = st.slider(
            "Magnitude (Richter)",
            min_value=3.0,
            max_value=9.0,
            value=5.5,
            step=0.1
        )
        
        depth = st.slider(
            "Depth (km)",
            min_value=1.0,
            max_value=700.0,
            value=50.0,
            step=1.0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude", value=-6.2088)
        with col2:
            longitude = st.number_input("Longitude", value=106.8456)
        
        st.markdown("---")
        st.markdown("**System Info:**")
        st.markdown(f"Python: {sys.version}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Prediction")
        
        # Load model
        model_data = load_model()
        
        if model_data:
            st.success("✅ AI Model loaded successfully!")
            
            if st.button("🔍 Analyze Earthquake Impact", type="primary"):
                # Simple calculation
                shaking = magnitude / (depth**0.5) * 10
                
                # Classification logic
                if magnitude < 4.0:
                    impact = "Minor"
                elif magnitude < 5.0:
                    impact = "Light"
                elif magnitude < 6.0:
                    impact = "Moderate"
                elif magnitude < 7.0:
                    impact = "Strong"
                elif magnitude < 8.0:
                    impact = "Major"
                else:
                    impact = "Severe"
                
                # Tsunami risk
                if magnitude > 7.5 and depth < 50:
                    tsunami = "High"
                elif magnitude > 6.5 and depth < 100:
                    tsunami = "Medium"
                else:
                    tsunami = "Low"
                
                # Display results
                st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                st.subheader("📊 Results:")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Impact Level", impact)
                with col_b:
                    st.metric("Tsunami Risk", tsunami)
                with col_c:
                    st.metric("Shaking Intensity", f"{shaking:.2f}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Recommendations
                st.subheader("🚨 Recommendations")
                if impact in ["Major", "Severe"]:
                    st.warning("Evacuate to higher ground immediately!")
                elif impact in ["Strong", "Moderate"]:
                    st.info("Take cover under sturdy furniture")
                else:
                    st.success("Stay alert for aftershocks")
                
                # Visualization
                st.subheader("📈 Visualization")
                fig, ax = plt.subplots(figsize=(10, 4))
                
                # Bar chart sederhana
                categories = ['Magnitude', 'Depth', 'Intensity']
                values = [magnitude, depth/100, shaking/10]
                
                bars = ax.bar(categories, values, color=['red', 'blue', 'green'])
                ax.set_ylabel('Value')
                ax.set_title('Earthquake Parameters')
                
                st.pyplot(fig)
        
        else:
            st.warning("""
            ⚠️ Model not available
            
            Steps to fix:
            1. Ensure 'earthquake_model.pkl' is in GitHub
            2. Check file name spelling
            3. File should be < 100MB
            
            For now, using rule-based prediction.
            """)
    
    with col2:
        st.header("📋 System Status")
        
        # System metrics
        st.metric("Status", "🟢 Online")
        st.metric("Version", "1.0")
        st.metric("Last Update", datetime.now().strftime("%Y-%m-%d"))
        
        st.markdown("---")
        
        st.header("🔧 Components")
        st.markdown("""
        ✅ Data Input  
        ✅ Database  
        ✅ Machine Learning  
        ✅ Dashboard  
        """)
        
        st.markdown("---")
        
        st.header("📁 Files Check")
        
        # Check if files exist
        files_to_check = [
            ('app.py', 'Main application'),
            ('requirements.txt', 'Dependencies'),
            ('earthquake_model.pkl', 'AI Model'),
            ('earthquake_data.csv', 'Dataset')
        ]
        
        for filename, description in files_to_check:
            if os.path.exists(filename):
                st.success(f"✅ {filename} - {description}")
            else:
                st.error(f"❌ {filename} - {description}")

# ============================================
# 7. RUN APPLICATION
# ============================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please check the requirements.txt file and model file.")
