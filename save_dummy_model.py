import pickle
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Dummy training data
# Features: [soil_nitrogen, soil_phosphorus, soil_potassium, rainfall, temperature]
X = np.array([
    [10, 5, 5, 100, 25],
    [20, 10, 10, 200, 27],
    [15, 8, 7, 150, 26],
    [25, 12, 11, 180, 28]
])

# Target: maize yield in tons/ha
y = np.array([2.5, 3.8, 3.0, 4.0])

# Train dummy model
model = RandomForestRegressor()
model.fit(X, y)

# Save the model
with open("models/maize_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Dummy model saved as maize_model.pkl")
