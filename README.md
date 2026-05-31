# 🌱 Precision Agriculture: Soil Health & Fertilizer Optimization

![Precision Agriculture Banner](https://img.shields.io/badge/Precision%20Agriculture-Data%20Analytics-2E7D32?style=for-the-badge&logo=appveyor)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)

A comprehensive data analytics and Exploratory Data Analysis (EDA) platform designed to promote sustainable agriculture. This project analyzes soil properties (NPK levels, pH, organic carbon) and provides actionable insights for fertilizer optimization to reduce environmental impact and improve crop yield.

---

## 🎯 Main Problem Statement

Modern agriculture relies heavily on chemical fertilizers, leading to over-fertilization, soil degradation, and water pollution. Adding more fertilizer does not always increase crop yield; after a certain threshold, it becomes ineffective (diminishing returns) and ecologically harmful.

This project uses **data-driven analytics** to identify:
- Nutrient deficiencies and excesses.
- The threshold of diminishing returns for fertilizer usage.
- Relationships between soil health and crop yield.
- Electrical Conductivity (EC) risk zones and pest outbreak triggers.

## ✨ Features

The platform consists of a fully interactive **Streamlit Dashboard** offering 8 advanced modules:
1. **Dataset Overview:** Raw data shape, statistics, and missing values check.
2. **NPK Analysis:** Distributions of Nitrogen, Phosphorus, and Potassium using interactive histograms and boxplots.
3. **Soil Health Dashboard:** Monitoring pH, Organic Carbon, and Electrical Conductivity with a dynamic correlation heatmap.
4. **Yield Analysis (Diminishing Returns):** Scatterplots clearly visualizing the threshold where excess fertilizer degrades crop yield.
5. **Climate Impact:** Multivariate analysis of temperature, rainfall, and sunlight on crop productivity.
6. **Pest Risk Analysis:** Identifying environmental triggers (e.g., high humidity + excess nitrogen) that lead to pest outbreaks.
7. **Personalized Soil Report Card:** A simulator that calculates a composite Soil Health Score (0-100) and outputs actionable recommendations based on soil metrics.

## 📂 Project Structure

```text
crop_EDA/
├── data/
│   ├── raw/                  # Raw CSV datasets
│   └── processed/            # Cleaned and augmented datasets
├── src/
│   ├── preprocessing.py      # Data cleaning and standardization logic
│   ├── data_augmentation.py  # Feature engineering & synthetic data generation
│   ├── eda_analysis.py       # Core EDA and matplotlib/seaborn visualization logic
│   └── main.py               # CLI entry point to run the data pipeline
├── visuals/                  # Generated plots and static charts
├── app.py                    # Main Streamlit dashboard application
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 🛠️ Technology Stack

- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **Data Processing:** Pandas, NumPy
- **Visualizations:** Plotly Express, Seaborn, Matplotlib
- **Machine Learning (Lightweight):** Scikit-learn, Statsmodels

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/precision-agriculture-eda.git
cd precision-agriculture-eda
```

### 2. Install dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Run the Data Pipeline (Optional)
If you want to re-run the cleaning and feature engineering pipeline to regenerate the dataset:
```bash
python src/main.py
```
To generate the static EDA charts inside the `visuals/` folder:
```bash
python src/eda_analysis.py
```

### 4. Launch the Dashboard
```bash
streamlit run app.py
```

## 📊 Key Insights Extracted
- **Diminishing Returns:** Yield increases with optimal Nitrogen and Phosphorus but sharply degrades once the toxicity threshold is reached.
- **Salinity Risks:** Electrical Conductivity (EC) increases linearly with total fertilizer, highlighting severe over-fertilization zones.
- **Pest Vulnerability:** High humidity combined with excessive nitrogen application creates a massive compounding effect on pest incidence.

---

*Designed for Sustainable Agriculture.*
