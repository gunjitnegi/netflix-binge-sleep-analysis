import pandas as pd
import numpy as np


df = pd.read_csv('data/raw/netflix_sleep_data_raw.csv')                              #loading raw data

print("Initial Data Overview:")
print(df.info())
print(df.head())

# Handle missing values

df = df.dropna(subset=['Sleep Start Time', 'Sleep End Time', 'Total Sleep Duration (hrs)','Episode Start Time', 'Last Episode End Time', 'Total Viewing Time (hrs)'])                 # Drop rows where essential info is missing

#Fill missing numerical values with median
numeric_cols = [ 'Total Sleep Duration (hrs)', 'Total Viewing Time (hrs)', 'Time From Last Episode to Sleep (mins)']
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())


# Step 3: Correct data types
time_cols = ['Sleep Start Time', 'Sleep End Time', 'Episode Start Time', 'Last Episode End Time']
for col in time_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Remove rows where datetime conversion failed
df = df.dropna(subset=time_cols)

for col in numeric_cols:
    df[col] = df[col].astype(float)


# Step 4: Remove duplicates

df = df.drop_duplicates()

# Step 5: Save cleaned data

df.to_csv('data/processed/netflix_sleep_cleaned.csv', index=False)
print("Cleaned data saved to data/processed/netflix_sleep_cleaned.csv")
print(f"Dropped rows logged to data/processed/dropped_rows_log.csv")
