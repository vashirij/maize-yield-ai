import pandas as pd
from sklearn.preprocessing import StandardScaler

# === Load the CSV files ===
yield_df = pd.read_csv("maize_yield.csv")
weather_df = pd.read_csv("weather.csv")

# === Preview and clean column names ===
yield_df.columns = yield_df.columns.str.strip()
weather_df.columns = weather_df.columns.str.strip()

# === Merge datasets on 'Year' ===
merged_df = pd.merge(yield_df, weather_df, on='Year', how='inner')

# === Check and handle missing values ===
merged_df.dropna(inplace=True)

# === Optional: Convert to correct dtypes if needed ===
merged_df['Year'] = merged_df['Year'].astype(int)
merged_df['Maize yield'] = pd.to_numeric(merged_df['Maize yield'], errors='coerce')

# === Normalize numeric features for modeling ===
scaler = StandardScaler()
features_to_scale = ['Average Temperature', 'Average Relative Humidity', 'Average Rain (mm)']
merged_df[features_to_scale] = scaler.fit_transform(merged_df[features_to_scale])

# === Save the final dataset ===
merged_df.to_csv("Final_Data3.csv", index=False)

print(" Preprocessing complete. File saved as 'Final_Data.csv'.")
