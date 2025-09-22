
import pandas as pd

# -----------------------------
# Step 1: Load cleaned data
# -----------------------------
df = pd.read_csv('data/processed/netflix_sleep_cleaned.csv')

# -----------------------------
# Step 2: Convert decimal hours to HH:MM format
# -----------------------------
def decimal_to_hhmm(x):
    hours = int(x)
    minutes = int(round((x - hours) * 60))
    return f"{hours}:{minutes:02d}"

df['Sleep_Duration_HHMM'] = df['Total Sleep Duration (hrs)'].apply(decimal_to_hhmm)
df['Viewing_Time_HHMM'] = df['Total Viewing Time (hrs)'].apply(decimal_to_hhmm)

# -----------------------------
# Step 3: Late-night Netflix flag
# -----------------------------
df['Last Episode End Time'] = pd.to_datetime(df['Last Episode End Time'])
df['Late_Night_Viewing'] = df['Last Episode End Time'].dt.hour >= 23

# -----------------------------
# Step 4: Viewing duration categories
# -----------------------------
def viewing_category(x):
    if x < 1:
        return 'Short'
    elif x <= 3:
        return 'Medium'
    else:
        return 'Long'

df['Viewing_Category'] = df['Total Viewing Time (hrs)'].apply(viewing_category)

# -----------------------------
# Step 5: Weekday vs Weekend
# -----------------------------
df['Sleep Start Time'] = pd.to_datetime(df['Sleep Start Time'])
df['Is_Weekend'] = df['Sleep Start Time'].dt.day_name().isin(['Saturday', 'Sunday'])

# -----------------------------
# Step 6: Gap between last episode and sleep in HH:MM
# -----------------------------
df['Gap_Last_Episode_to_Sleep_HHMM'] = df['Time From Last Episode to Sleep (mins)'].apply(
    lambda x: f"{int(x//60)}:{int(x%60):02d}"
)

# -----------------------------
# Step 7: Night binge indicator
# -----------------------------
# Define night binge: viewing >3 hrs and ends after 11 PM
df['Night_Binge'] = (df['Total Viewing Time (hrs)'] > 3) & (df['Last Episode End Time'].dt.hour >= 23)

# -----------------------------
# Step 8: Sleep deprivation flag
# -----------------------------
# Sleep <5 hrs
df['Sleep_Deprivation'] = df['Total Sleep Duration (hrs)'] < 5

# -----------------------------
# Step 9: Sleep Score (1-10)
# -----------------------------

df['Sleep Start Time'] = pd.to_datetime(df['Sleep Start Time'], errors='coerce')
df['Sleep End Time'] = pd.to_datetime(df['Sleep End Time'], errors='coerce')

def calculate_sleep_score(row):
    score = 10
    sleep_duration = row['Total Sleep Duration (hrs)']
    sleep_start = row['Sleep Start Time']
    sleep_end = row['Sleep End Time']

    # Penalize short sleep
    if sleep_duration < 5:
        score -= 4
    elif sleep_duration < 6:
        score -= 2

    # Penalize late sleep
    if sleep_start.hour >= 2:
        score -= 2
    elif sleep_start.hour >= 0:
        score -= 1

    # Penalize waking very early with short sleep
    if sleep_end.hour < 6 and sleep_duration < 6:
        score -= 2

    return max(1, min(10, score))

df['Sleep_Score'] = df.apply(calculate_sleep_score, axis=1)

# -----------------------------
# Step 10: Save feature engineered dataset
# -----------------------------
df.to_csv('data/processed/netflix_sleep_features.csv', index=False)
print("Feature engineered dataset saved to data/processed/netflix_sleep_features.csv")
