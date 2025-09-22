# Netflix Binge Patterns & Sleep Disruption Analysis

This project analyzes how Netflix binge-watching affects sleep patterns using personal data. It combines **data cleaning, feature engineering, visualization, machine learning, and scenario simulation** to provide insights into sleep quality and binge behavior trends.

---

## **Project Motivation**

Modern streaming habits often disrupt sleep, but most observations are anecdotal. This project quantifies the relationship between Netflix viewing habits and sleep duration, providing **data-driven insights** into how binge-watching impacts sleep quality.

---

## **Project Structure**

netflixbinge/
│
├── data/
│ ├── raw/ # Raw CSV files (original data)
│ └── processed/ # Cleaned and feature-engineered datasets
├── scripts/
│ ├── clean_data.py # Cleans raw data
│ ├── feature_engineering.py # Generates features like Sleep Score, Night Binge flags
│ ├── analyze_sleep_binge.py # Visualizations & descriptive statistics
│ └── netflix_sleep_ml_simulation.py # Predictive ML & "what-if" scenario simulation
├── notebooks/ # Optional Jupyter notebooks for exploration
├── README.md
└── requirements.txt

## **Data Cleaning & Feature Engineering**

Key steps include:

- Handling missing values and duplicates
- Converting timestamp columns to datetime objects
- Feature engineering:
  - **Sleep Score (1–10)** based on sleep duration and timing
  - **Sleep Deprivation Flag** for short sleep duration
  - **Night Binge Indicator** (late-night binge watching)
  - **Weekday/Weekend Flag**
  - **Viewing Duration Categories**: Short (<1 hr), Medium (1–3 hrs), Long (>3 hrs)
  - **Late-Night Netflix Flag**
  - **Gap Between Last Episode and Sleep** (HH:MM)

---

## **Visualizations**

- **Scatter plots** of Netflix duration vs sleep hours
- **Heatmaps** of binge time vs sleep onset
- **Time series plots** to see trends over time
- **Correlation matrices** of sleep and binge metrics

---

## **Machine Learning & Simulation**

- Predict **sleep duration** based on viewing patterns using **Random Forest Regressor**
- Simulate **“what-if” scenarios** to evaluate:
  - Sleep loss if binge continues for multiple days
  - Sleep Score under continued binge behavior
- Visualize predicted trends for sleep duration and sleep score

---

## **Key Insights**

- Clear quantification of the relationship between **total viewing time** and **sleep duration**
- Identification of **high-risk binge habits** that reduce sleep quality
- Data-driven recommendations for better **sleep hygiene**

---

## **How to Run**

1. Clone the repository:

```bash
git clone https://github.com/your-username/netflix-binge-sleep-analysis.git
cd netflix-binge-sleep-analysis

2. Create a virtual environment (optional but recommended):

python -m venv venv
# Activate the environment:
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate


3. Install dependencies:

pip install -r requirements.txt


4. Run scripts in order:

python scripts/clean_data.py
python scripts/feature_engineering.py
python scripts/analyze_sleep_binge.py
python scripts/netflix_sleep_ml_simulation.py