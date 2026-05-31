"""
Data Preprocessing Module
Handles data loading, cleaning, validation, and preparation for analysis.
"""

import pandas as pd
import numpy as np
import logging
import os

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_data(filepath):
    """
    Load dataset from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame or None: Loaded dataset or None if failed.
    """
    logging.info(f"Attempting to load dataset from {filepath}...")
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found at {filepath}")
        df = pd.read_csv(filepath)
        if df.empty:
            raise ValueError("The dataset is empty.")
        logging.info("Dataset loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"Error loading dataset: {e}")
        return None

def validate_dataset(df):
    """
    Validate dataset structure, display shape and columns.
    
    Args:
        df (pd.DataFrame): The dataset to validate.
    """
    logging.info("Validating dataset structure...")
    logging.info(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    logging.info(f"Dataset Columns: {list(df.columns)}")
    return True

def standardize_columns(df):
    """
    Standardize column names (lowercase, replace spaces with underscores).
    Convert categorical columns to string type if necessary.
    
    Args:
        df (pd.DataFrame): Raw dataframe.
        
    Returns:
        pd.DataFrame: Dataframe with standardized columns.
    """
    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    logging.info("Standardized column names.")
    
    # Ensure categorical columns are strings and stripped of whitespace
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        df[col] = df[col].astype(str).str.strip()
        
    return df

def handle_missing_values(df):
    """
    Detect and handle missing values.
    Numeric columns are filled with median. Categorical columns are filled with mode.
    
    Args:
        df (pd.DataFrame): Dataframe to clean.
        
    Returns:
        pd.DataFrame: Dataframe without missing values.
    """
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        logging.info(f"Detected {missing_count} missing values. Handling them...")
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    median_val = df[col].median()
                    df[col] = df[col].fillna(median_val)
                else:
                    mode_val = df[col].mode()[0]
                    df[col] = df[col].fillna(mode_val)
        logging.info("Missing values handled successfully.")
    else:
        logging.info("No missing values detected.")
    return df

def remove_duplicates(df):
    """
    Remove duplicate rows from the dataset.
    
    Args:
        df (pd.DataFrame): Dataframe to clean.
        
    Returns:
        pd.DataFrame: Dataframe without duplicates.
    """
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        logging.info(f"Removed {duplicates} duplicate rows.")
    else:
        logging.info("No duplicate rows detected.")
    return df

def detect_outliers(df):
    """
    Detect outliers using the Interquartile Range (IQR) method for numeric columns.
    Values outside the bounds are capped to maintain consistency without losing rows.
    
    Args:
        df (pd.DataFrame): Dataframe to process.
        
    Returns:
        pd.DataFrame: Dataframe with capped outliers.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers_detected = False
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Detect outliers
        outlier_condition = (df[col] < lower_bound) | (df[col] > upper_bound)
        count = outlier_condition.sum()
        if count > 0:
            outliers_detected = True
            logging.info(f"Detected {count} outliers in column '{col}'. Capping values.")
            
            # Cap the outliers safely
            df.loc[df[col] < lower_bound, col] = lower_bound
            df.loc[df[col] > upper_bound, col] = upper_bound

    if not outliers_detected:
        logging.info("No extreme outliers detected in numeric columns.")
        
    return df

def save_processed_data(df, output_filepath):
    """
    Save the cleaned dataset to a CSV file.
    
    Args:
        df (pd.DataFrame): Processed dataframe to save.
        output_filepath (str): Target path.
    """
    try:
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        df.to_csv(output_filepath, index=False)
        logging.info(f"Processed dataset saved successfully to {output_filepath}")
    except Exception as e:
        logging.error(f"Error saving processed data: {e}")

def clean_data(df):
    """
    Clean the dataset by executing the full preprocessing pipeline.
    
    Args:
        df (pd.DataFrame): Raw dataframe.
        
    Returns:
        pd.DataFrame: Cleaned and preprocessed dataframe.
    """
    logging.info("Starting data cleaning pipeline...")
    if df is None or df.empty:
        logging.error("Cannot clean an empty or None dataset.")
        return None
        
    validate_dataset(df)
    df = standardize_columns(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = detect_outliers(df)
    
    logging.info("Data cleaning pipeline completed successfully.")
    return df
