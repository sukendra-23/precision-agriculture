"""
Data Augmentation Module
Expands the dataset by creating additional meaningful agricultural features.
"""

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def generate_fertilizer_usage(df):
    """
    Generate Nitrogen, Phosphorus, and Potassium applied based on current soil levels.
    """
    np.random.seed(42)
    # Assume 30-50% loss into the environment/plant uptake, so applied > current soil level
    df['nitrogen_applied_kg_per_ha'] = df['nitrogen'] * np.random.uniform(1.2, 1.8, len(df)) + np.random.normal(10, 5, len(df))
    df['phosphorus_applied_kg_per_ha'] = df['phosphorus'] * np.random.uniform(1.1, 1.5, len(df)) + np.random.normal(5, 2, len(df))
    df['potassium_applied_kg_per_ha'] = df['potassium'] * np.random.uniform(1.1, 1.4, len(df)) + np.random.normal(8, 3, len(df))
    
    # Ensure no negative values
    df['nitrogen_applied_kg_per_ha'] = df['nitrogen_applied_kg_per_ha'].clip(lower=0)
    df['phosphorus_applied_kg_per_ha'] = df['phosphorus_applied_kg_per_ha'].clip(lower=0)
    df['potassium_applied_kg_per_ha'] = df['potassium_applied_kg_per_ha'].clip(lower=0)
    
    logging.info("Generated fertilizer usage columns successfully.")
    return df

def generate_soil_moisture(df):
    """
    Generate soil moisture % correlated with rainfall and humidity.
    """
    np.random.seed(43)
    # Normalizing rainfall and humidity roughly
    base_moisture = (df['rainfall'] * 0.1) + (df['humidity'] * 0.4) + np.random.normal(10, 5, len(df))
    df['soil_moisture_pct'] = base_moisture.clip(lower=10, upper=95)
    logging.info("Generated soil moisture percentage successfully.")
    return df

def generate_organic_carbon(df):
    """
    Generate organic carbon percentage based on soil type.
    """
    np.random.seed(44)
    def carbon_by_soil(soil):
        soil_lower = str(soil).lower()
        if 'peaty' in soil_lower:
            return np.random.uniform(4.0, 8.0)
        elif 'clay' in soil_lower:
            return np.random.uniform(1.5, 3.0)
        elif 'loamy' in soil_lower:
            return np.random.uniform(1.0, 2.5)
        elif 'sandy' in soil_lower:
            return np.random.uniform(0.1, 1.0)
        else:
            return np.random.uniform(0.5, 2.0)
            
    df['organic_carbon_pct'] = df['soil_type'].apply(carbon_by_soil)
    logging.info("Generated organic carbon percentage successfully.")
    return df

def generate_ec_level(df):
    """
    Generate Electrical Conductivity (EC) derived from fertilizer application.
    High fertilizer increases EC.
    """
    np.random.seed(45)
    total_fert = df['nitrogen_applied_kg_per_ha'] + df['phosphorus_applied_kg_per_ha'] + df['potassium_applied_kg_per_ha']
    # Base EC around 0.3 - 1.2 dS/m, increases by a factor of total fertilizer applied
    df['electrical_conductivity'] = np.random.uniform(0.3, 1.2, len(df)) + (total_fert * 0.003)
    logging.info("Generated electrical conductivity (EC) successfully.")
    return df

def generate_environmental_factors(df):
    """
    Generate sunlight hours and irrigation frequency.
    """
    np.random.seed(46)
    # Sunlight correlates slightly with temperature
    df['sunlight_hours'] = (df['temperature'] * 0.15) + np.random.uniform(4, 7, len(df))
    df['sunlight_hours'] = df['sunlight_hours'].clip(lower=4, upper=14)
    
    # Irrigation frequency (days between watering) - inversely related to soil moisture
    df['irrigation_frequency_days'] = 25 - (df['soil_moisture_pct'] * 0.2) + np.random.normal(0, 2, len(df))
    df['irrigation_frequency_days'] = df['irrigation_frequency_days'].clip(lower=1, upper=30).round()
    
    logging.info("Generated environmental factors (sunlight, irrigation) successfully.")
    return df

def generate_pest_incidence(df):
    """
    Generate pest incidence % based on high humidity and excess nitrogen.
    """
    np.random.seed(47)
    pest_risk = (df['humidity'] * 0.2) + (df['nitrogen_applied_kg_per_ha'] * 0.1) + np.random.normal(0, 5, len(df))
    df['pest_incidence_pct'] = pest_risk.clip(lower=0, upper=100)
    logging.info("Generated pest incidence percentage successfully.")
    return df

def generate_yield(df):
    """
    Generate realistic crop yield incorporating diminishing returns of fertilizers.
    """
    np.random.seed(48)
    
    N = df['nitrogen_applied_kg_per_ha']
    P = df['phosphorus_applied_kg_per_ha']
    K = df['potassium_applied_kg_per_ha']
    
    # Diminishing returns formula
    n_effect = 20 * N - 0.06 * (N ** 2)
    p_effect = 30 * P - 0.15 * (P ** 2)
    k_effect = 25 * K - 0.10 * (K ** 2)
    
    moisture_effect = df['soil_moisture_pct'] * 15
    pest_effect = df['pest_incidence_pct'] * -20
    
    base_yield = np.random.normal(1000, 200, len(df))
    
    total_yield = base_yield + n_effect + p_effect + k_effect + moisture_effect + pest_effect
    
    df['yield_kg_per_hectare'] = total_yield.clip(lower=500, upper=15000)
    
    logging.info("Generated yield with diminishing returns successfully.")
    return df

def augment_dataset(df):
    """
    Main orchestration function for feature engineering.
    """
    logging.info("Feature generation started...")
    
    if df is None or df.empty:
        logging.error("Cannot augment an empty dataset.")
        return df
        
    df = df.copy()
    
    df = generate_fertilizer_usage(df)
    df = generate_soil_moisture(df)
    df = generate_organic_carbon(df)
    df = generate_ec_level(df)
    df = generate_environmental_factors(df)
    df = generate_pest_incidence(df)
    df = generate_yield(df)
    
    logging.info("Dataset expansion completed.")
    return df
