"""
CLI Entry Point for Precision Agriculture Pipeline
Executes the data preprocessing and augmentation pipeline.
"""

import os
import sys
import logging
from preprocessing import load_data, clean_data, save_processed_data
from data_augmentation import augment_dataset

# Ensure logging is set up
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_pipeline():
    """
    Main function to execute the end-to-end data processing and analysis pipeline.
    """
    print("=" * 60)
    print("🌱 Starting Precision Agriculture Preprocessing & Augmentation 🌱")
    print("=" * 60)
    
    # Define file paths relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_filepath = os.path.join(base_dir, 'data', 'raw', 'sensor_Crop_Dataset (1).csv')
    output_filepath = os.path.join(base_dir, 'data', 'processed', 'cleaned_soil_data.csv')
    
    # 1. Load Data
    print("\n--- STEP 1: Data Loading ---")
    df = load_data(input_filepath)
    if df is None:
        logging.error("Pipeline stopped due to data loading failure.")
        sys.exit(1)
        
    # 2. Clean & Preprocess Data
    print("\n--- STEP 2: Data Preprocessing ---")
    cleaned_df = clean_data(df)
    
    if cleaned_df is None:
        logging.error("Pipeline stopped due to preprocessing failure.")
        sys.exit(1)
        
    # 3. Data Augmentation (Feature Engineering)
    print("\n--- STEP 3: Data Augmentation ---")
    augmented_df = augment_dataset(cleaned_df)
    
    # 4. Save Processed Data
    print("\n--- STEP 4: Saving Dataset ---")
    if augmented_df is not None:
        save_processed_data(augmented_df, output_filepath)
        
        # Print Final Summary
        print("=" * 60)
        print("✅ Preprocessing & Augmentation Complete!")
        print(f"Original Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"Final Augmented Dataset Shape: {augmented_df.shape[0]} rows, {augmented_df.shape[1]} columns")
        print("\nFinal Dataset Columns:")
        for col in augmented_df.columns:
            print(f"  - {col}")
        print(f"\nProcessed file is ready in: {output_filepath}")
        print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
