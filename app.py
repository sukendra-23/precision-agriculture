"""
Precision Agriculture Intelligence System - Streamlit Dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# -----------------------------------------
# Page Configuration
# -----------------------------------------
st.set_page_config(
    page_title="Precision Ag Dashboard", 
    page_icon="🌱", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# Data Loading
# -----------------------------------------
@st.cache_data
def load_dataset():
    """
    Load the cleaned dataset from data/processed/
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, 'data', 'processed', 'cleaned_soil_data.csv')
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        st.error(f"Processed dataset not found at: {filepath}")
        st.warning("Please ensure you have run the preprocessing pipeline first.")
        return None

# -----------------------------------------
# Main Application / Sidebar Navigation
# -----------------------------------------
def main():
    df = load_dataset()
    if df is None:
        return
        
    # Sidebar Styling & Navigation
    st.sidebar.title("🌱 Precision Ag")
    st.sidebar.markdown("---")
    
    pages = [
        "Home",
        "Dataset Overview",
        "NPK Analysis",
        "Soil Health Dashboard",
        "Yield Analysis",
        "Climate Impact",
        "Pest Risk Analysis",
        "Soil Report Card"
    ]
    
    selection = st.sidebar.radio("Navigation", pages)
    
    # Page Routing
    if selection == "Home":
        render_home(df)
    elif selection == "Dataset Overview":
        render_dataset_overview(df)
    elif selection == "NPK Analysis":
        render_npk_analysis(df)
    elif selection == "Soil Health Dashboard":
        render_soil_health(df)
    elif selection == "Yield Analysis":
        render_yield_analysis(df)
    elif selection == "Climate Impact":
        render_climate_impact(df)
    elif selection == "Pest Risk Analysis":
        render_pest_risk(df)
    elif selection == "Soil Report Card":
        render_soil_report_card(df)

# -----------------------------------------
# Page Render Functions
# -----------------------------------------
def render_home(df):
    st.title("Precision Agriculture Intelligence System")
    st.markdown("Welcome to the advanced analytics platform designed to optimize fertilizer usage, monitor soil health, and maximize crop yields sustainably.")
    
    # Key Insight Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📈 **Yield Optimization**\nIdentify the exact threshold where fertilizer boosts yield before causing diminishing returns.")
    with col2:
        st.success("🌱 **Soil Health Monitoring**\nTrack pH, Organic Carbon, and Electrical Conductivity (EC) to prevent soil degradation.")
    with col3:
        st.warning("📉 **Fertilizer Reduction**\nReduce environmental impact and save costs by avoiding over-fertilization.")
        
    st.markdown("---")
    st.subheader("Dataset Summary At a Glance")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Total Records", f"{df.shape[0]:,}")
    metric_col2.metric("Total Features", df.shape[1])
    metric_col3.metric("Crops Analyzed", df['crop'].nunique() if 'crop' in df.columns else "N/A")

def render_dataset_overview(df):
    st.title("Dataset Overview")
    st.markdown("Review the raw dimensions, first rows, and statistical summaries of your processed dataset.")
    
    st.write(f"### Data Shape: `{df.shape[0]} rows` × `{df.shape[1]} columns`")
    
    st.write("### First 10 Rows")
    st.dataframe(df.head(10), use_container_width=True)
    
    st.write("### Summary Statistics")
    st.dataframe(df.describe().T, use_container_width=True)
    
    missing = df.isnull().sum().sum()
    if missing == 0:
        st.success("✅ Missing Values: 0 (Dataset is perfectly clean)")
    else:
        st.warning(f"Missing Values: {missing}")

def render_npk_analysis(df):
    st.title("NPK Distribution Analysis")
    st.markdown("Analyze the distribution of Nitrogen, Phosphorus, and Potassium in the soil.")
    
    nutrients = ['nitrogen', 'phosphorus', 'potassium']
    selected_nutrient = st.selectbox("Select Nutrient to Visualize", nutrients)
    
    col1, col2 = st.columns(2)
    with col1:
        fig_hist = px.histogram(df, x=selected_nutrient, nbins=50, 
                                title=f"{selected_nutrient.capitalize()} Histogram", 
                                color_discrete_sequence=['#4CAF50'])
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col2:
        fig_box = px.box(df, y=selected_nutrient, 
                         title=f"{selected_nutrient.capitalize()} Boxplot", 
                         color_discrete_sequence=['#81C784'])
        st.plotly_chart(fig_box, use_container_width=True)
        
    st.info(f"💡 Optimal zones for {selected_nutrient.capitalize()} vary by crop, but extreme outliers on the right indicate potential over-fertilization zones.")

def render_soil_health(df):
    st.title("Soil Health Dashboard")
    st.markdown("Monitor critical soil indicators and feature correlations.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig1 = px.histogram(df, x="ph_value", title="pH Distribution", color_discrete_sequence=['#AB47BC'])
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        if 'organic_carbon_pct' in df.columns:
            fig2 = px.histogram(df, x="organic_carbon_pct", title="Organic Carbon (%)", color_discrete_sequence=['#8D6E63'])
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Organic Carbon data not found.")
            
    with col3:
        if 'electrical_conductivity' in df.columns:
            fig3 = px.histogram(df, x="electrical_conductivity", title="Electrical Conductivity (EC)", color_discrete_sequence=['#FFA726'])
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("EC data not found.")
            
    st.markdown("---")
    st.subheader("Correlation Heatmap")
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    fig_heat = px.imshow(corr, text_auto=False, aspect="auto", color_continuous_scale='RdYlGn', title="Numeric Feature Correlations")
    st.plotly_chart(fig_heat, use_container_width=True)

def render_yield_analysis(df):
    st.title("Yield Analysis & Diminishing Returns")
    st.markdown("Visualize the impact of applied fertilizer on crop yield. Notice the diminishing returns curve where excess fertilizer degrades yield.")
    
    fert_options = {
        "Nitrogen Applied": "nitrogen_applied_kg_per_ha", 
        "Phosphorus Applied": "phosphorus_applied_kg_per_ha", 
        "Potassium Applied": "potassium_applied_kg_per_ha"
    }
    
    # Check if columns exist
    available_options = {k: v for k, v in fert_options.items() if v in df.columns}
    
    if not available_options:
        st.error("Fertilizer application columns not found. Ensure dataset augmentation ran correctly.")
        return
        
    fert_choice = st.radio("Select Fertilizer to Analyze:", list(available_options.keys()), horizontal=True)
    selected_col = available_options[fert_choice]
    
    # We sample the dataset to make the scatter plot render faster and cleaner
    sample_df = df.sample(n=min(5000, len(df)), random_state=42)
    
    fig = px.scatter(sample_df, x=selected_col, y="yield_kg_per_hectare", 
                     opacity=0.3, title=f"Yield vs {fert_choice}", 
                     trendline="lowess", trendline_color_override="red",
                     color_discrete_sequence=['#1E88E5'])
                     
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("📉 The red trendline demonstrates the diminishing returns effect: yield peaks at an optimal fertilizer level and then declines due to toxicity and salinity.")

def render_climate_impact(df):
    st.title("Climate Impact Analysis")
    st.markdown("Explore how environmental factors affect yield and pest risks.")
    
    # Sample for rendering speed
    sample_df = df.sample(n=min(5000, len(df)), random_state=42)
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.scatter(sample_df, x="temperature", y="yield_kg_per_hectare", opacity=0.3, title="Temperature vs Yield", color_discrete_sequence=['#EF5350'])
        st.plotly_chart(fig1, use_container_width=True)
        
        if 'sunlight_hours' in df.columns:
            fig2 = px.scatter(sample_df, x="sunlight_hours", y="yield_kg_per_hectare", opacity=0.3, title="Sunlight vs Yield", color_discrete_sequence=['#FFA726'])
            st.plotly_chart(fig2, use_container_width=True)
        
    with col2:
        fig3 = px.scatter(sample_df, x="rainfall", y="yield_kg_per_hectare", opacity=0.3, title="Rainfall vs Yield", color_discrete_sequence=['#42A5F5'])
        st.plotly_chart(fig3, use_container_width=True)
        
        if 'pest_incidence_pct' in df.columns:
            fig4 = px.scatter(sample_df, x="humidity", y="pest_incidence_pct", opacity=0.3, title="Humidity vs Pest Incidence", color_discrete_sequence=['#7E57C2'])
            st.plotly_chart(fig4, use_container_width=True)

def render_pest_risk(df):
    st.title("Pest Risk Analysis")
    st.markdown("Identify the conditions that trigger pest outbreaks.")
    
    if 'pest_incidence_pct' not in df.columns or 'nitrogen_applied_kg_per_ha' not in df.columns:
        st.error("Required columns for Pest Risk Analysis are missing.")
        return
        
    sample_df = df.sample(n=min(3000, len(df)), random_state=42)
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.scatter(sample_df, x="humidity", y="pest_incidence_pct", opacity=0.3, trendline="ols", title="Humidity vs Pests", color_discrete_sequence=['#5C6BC0'])
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        fig2 = px.scatter(sample_df, x="nitrogen_applied_kg_per_ha", y="pest_incidence_pct", opacity=0.3, trendline="ols", title="Nitrogen Applied vs Pests", color_discrete_sequence=['#EF5350'])
        st.plotly_chart(fig2, use_container_width=True)
        
    st.warning("⚠️ **Key Insight:** High humidity combined with excessive nitrogen application significantly increases the risk of pest outbreaks.")

def render_soil_report_card(df):
    st.title("Personalized Soil Health Report Card")
    st.markdown("Select a sample from the dataset to generate a personalized health and optimization report.")
    
    sample_idx = st.number_input(f"Enter Sample ID (Row Number 0 to {len(df)-1})", min_value=0, max_value=len(df)-1, value=0, step=1)
    
    sample = df.iloc[sample_idx]
    
    # Safely extract metrics
    def get_val(col):
        return sample[col] if col in sample else 0
        
    total_fert = get_val('nitrogen_applied_kg_per_ha') + get_val('phosphorus_applied_kg_per_ha') + get_val('potassium_applied_kg_per_ha')
    ec = get_val('electrical_conductivity')
    pest = get_val('pest_incidence_pct')
    org_carbon = get_val('organic_carbon_pct')
    yield_val = get_val('yield_kg_per_hectare')
    ph = get_val('ph_value')
    moisture = get_val('soil_moisture_pct')
    
    # Calculate simple simulated score
    score = 100 - (ec * 10) - (pest * 0.2)
    score = max(0, min(100, score))
    
    # Logic classifications
    fertility_level = "High" if org_carbon > 2 else ("Medium" if org_carbon > 1 else "Low")
    yield_potential = "High" if yield_val > 8000 else ("Medium" if yield_val > 4000 else "Low")
    risk_level = "High" if pest > 50 or ec > 1.0 else ("Medium" if pest > 30 else "Low")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Current Metrics")
        st.write(f"**Crop:** `{sample.get('crop', 'N/A')}`")
        st.write(f"**Soil Type:** `{sample.get('soil_type', 'N/A')}`")
        st.write(f"**pH Value:** `{ph:.2f}`")
        st.write(f"**Electrical Conductivity (EC):** `{ec:.2f} dS/m`")
        st.write(f"**Organic Carbon:** `{org_carbon:.2f}%`")
        st.write(f"**Total Fertilizer Applied:** `{total_fert:.2f} kg/ha`")
        st.write(f"**Pest Incidence:** `{pest:.1f}%`")
        
    with col2:
        st.subheader("🏆 Assessment & Score")
        st.metric("Overall Soil Health Score", f"{score:.0f}/100")
        st.write(f"**Fertility Level:** `{fertility_level}`")
        st.write(f"**Yield Potential:** `{yield_potential}`")
        st.write(f"**Risk Level:** `{risk_level}`")
        
    st.divider()
    st.subheader("💡 Actionable Recommendations")
    
    if ec > 1.0 or total_fert > 300:
        st.error("📉 **Reduce Fertilizer:** High EC detected. You are over-fertilizing, causing soil salinity and diminishing returns.")
    else:
        st.success("✅ **Fertilizer:** Fertilizer usage is within safe bounds.")
        
    if moisture < 30:
        st.warning("💧 **Irrigation:** Soil moisture is low. Consider increasing irrigation frequency.")
        
    if ph < 5.5:
        st.warning("🧪 **pH Adjustment:** Soil is too acidic. Consider applying agricultural lime.")
    elif ph > 7.5:
        st.warning("🧪 **pH Adjustment:** Soil is too alkaline. Consider applying sulfur.")
        
    if pest > 40:
        st.error("🐛 **Pest Alert:** High pest incidence risk. Monitor crop closely and avoid excess nitrogen.")

if __name__ == "__main__":
    main()
