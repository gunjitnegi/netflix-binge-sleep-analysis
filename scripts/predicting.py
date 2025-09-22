import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


# Step 1: Load the feature-engineered dataset

df = pd.read_csv('data/processed/netflix_sleep_features.csv')

# Convert datetime columns
df['Sleep Start Time'] = pd.to_datetime(df['Sleep Start Time'])
df['Last Episode End Time'] = pd.to_datetime(df['Last Episode End Time'])

# Create numeric features
df['Sleep_Start_Hour'] = df['Sleep Start Time'].dt.hour
df['Last_Episode_End_Hour'] = df['Last Episode End Time'].dt.hour

# Encode boolean flags
df['Night_Binge'] = df['Night_Binge'].astype(int)
df['Late_Night_Viewing'] = df['Late_Night_Viewing'].astype(int)
df['Sleep_Deprivation'] = df['Sleep_Deprivation'].astype(int)
df['Is_Weekend'] = df['Is_Weekend'].astype(int)

# Features & Target
features = ['Total Viewing Time (hrs)', 'Night_Binge', 'Late_Night_Viewing',
            'Sleep_Start_Hour', 'Last_Episode_End_Hour',
            'Time From Last Episode to Sleep (mins)', 'Is_Weekend']
target = 'Total Sleep Duration (hrs)'

X = df[features]
y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 2: Train the Random Forest model

rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

# Evaluate model
y_pred = rf.predict(X_test)
print(f"\n✅ Model trained successfully.")
print(f"R² Score: {r2_score(y_test, y_pred):.3f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f} hrs\n")



# Helper function: Sleep Score

def calculate_sleep_score(sleep_duration, sleep_start_hour):
    score = 10
    if sleep_duration < 5:
        score -= 4
    elif sleep_duration < 6:
        score -= 2
    if sleep_start_hour >= 2:
        score -= 2
    elif sleep_start_hour >= 0:
        score -= 1
    if sleep_start_hour < 6 and sleep_duration < 6:
        score -= 2
    return max(1, min(10, score))



# Step 3: User Input

print("🔮 Netflix Sleep Impact Predictor")
print("Enter your planned binge details for tonight:")

# Get binge hours
hours = float(input("How many HOURS do you plan to binge? (e.g. 2.5): "))

# Flags
night_binge = input("Is it a NIGHT binge? (y/n): ").strip().lower() == "y"
late_night = input("Will it be LATE-NIGHT viewing (after midnight)? (y/n): ").strip().lower() == "y"
weekend = input("Is it a WEEKEND? (y/n): ").strip().lower() == "y"

# Timing details
sleep_start_hour = int(input("Approximate hour you plan to SLEEP (0-23, 24hr format): "))
last_episode_end_hour = int(input("Approximate hour you expect to FINISH binge (0-23): "))
gap_to_sleep = int(input("Gap from last episode to sleep in MINUTES (e.g. 15): "))


# Step 4: Make Prediction

user_data = pd.DataFrame([{
    'Total Viewing Time (hrs)': hours,
    'Night_Binge': int(night_binge),
    'Late_Night_Viewing': int(late_night),
    'Sleep_Start_Hour': sleep_start_hour,
    'Last_Episode_End_Hour': last_episode_end_hour,
    'Time From Last Episode to Sleep (mins)': gap_to_sleep,
    'Is_Weekend': int(weekend)
}])

predicted_sleep = rf.predict(user_data)[0]
predicted_score = calculate_sleep_score(predicted_sleep, sleep_start_hour)


# Step 5: Show Results

print("\n📊 Prediction Results:")
print(f"➡️ Predicted Sleep Duration: {predicted_sleep:.2f} hrs")
print(f"➡️ Predicted Sleep Score   : {predicted_score}/10")

# Additional interpretation
if predicted_sleep < 5:
    print("⚠️ High risk of sleep deprivation!")
elif predicted_sleep < 6.5:
    print("⚠️ Below recommended sleep – try to reduce binge hours.")
else:
    print("✅ Predicted sleep duration is within a healthy range.")
