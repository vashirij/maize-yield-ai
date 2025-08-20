from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle, numpy as np, pandas as pd, os, logging, requests, random

# Flask app config
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Logging
logging.basicConfig(filename="app.log", level=logging.INFO)

# Load model
MODEL_PATH = "maize_model.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Soil profiles for Marondera districts
soil_profiles = {
    "Chikomba":       {"soil_n": 25, "soil_p": 12, "soil_k": 18},
    "Goromonzi":      {"soil_n": 28, "soil_p": 14, "soil_k": 20},
    "Marondera":      {"soil_n": 30, "soil_p": 15, "soil_k": 22},
    "Mudzi":          {"soil_n": 22, "soil_p": 10, "soil_k": 16},
    "Murehwa":        {"soil_n": 27, "soil_p": 13, "soil_k": 19},
    "Mutoko":         {"soil_n": 24, "soil_p": 11, "soil_k": 17},
    "Seke":           {"soil_n": 29, "soil_p": 14, "soil_k": 21},
    "Uzumba-Maramba-Pfungwe": {"soil_n": 26, "soil_p": 12, "soil_k": 18},
    "Wedza":          {"soil_n": 23, "soil_p": 11, "soil_k": 16}
}

# Dummy coordinates for rainfall API
district_coords = {
    "Chikomba": (-19.0, 31.7),
    "Goromonzi": (-18.0, 31.2),
    "Marondera": (-18.2, 31.5),
    "Mudzi": (-16.9, 32.0),
    "Murehwa": (-17.5, 31.6),
    "Mutoko": (-17.3, 32.2),
    "Seke": (-18.0, 31.6),
    "Uzumba-Maramba-Pfungwe": (-17.7, 31.9),
    "Wedza": (-18.5, 31.9)
}

API_KEY = "YOUR_OPENWEATHERMAP_KEY"  # Replace with your key

# Allowed file check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Validate input
def validate_range(value, min_val=0, max_val=500):
    return min_val <= value <= max_val

# Fetch rainfall from OpenWeatherMap
def get_rainfall(district, api_key=API_KEY):
    lat, lon = district_coords[district]
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    total_rainfall = sum(day.get("rain", 0) for day in data.get("daily", []))
    return round(total_rainfall, 2)

# Routes
@app.route('/')
def home():
    return render_template('home.html', current_year=2025)

@app.route('/predict_page')
def predict_page():
    return render_template('index.html', soil_profiles=soil_profiles, current_year=2025)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        district = request.form.get('district')
        if district not in soil_profiles:
            return "Invalid district selected", 400

        # Auto soil nutrients
        soil_n = soil_profiles[district]['soil_n']
        soil_p = soil_profiles[district]['soil_p']
        soil_k = soil_profiles[district]['soil_k']

        # Rainfall from API
        rainfall = get_rainfall(district)

        # Temperature input
        temperature = float(request.form['temperature'])

        values = [soil_n, soil_p, soil_k, rainfall, temperature]
        if not all([validate_range(v) for v in values]):
            return "Invalid input values", 400

        pred = model.predict(np.array([values]))[0]
        logging.info(f"{district} prediction: {pred:.2f}")

        return render_template(
            'index.html',
            prediction=f"Estimated Yield: {pred:.2f} tons/ha",
            district=district,
            soil_n=soil_n,
            soil_p=soil_p,
            soil_k=soil_k,
            rainfall=rainfall,
            temperature=temperature,
            soil_profiles=soil_profiles,
            current_year=2025
        )
    except Exception as e:
        logging.error(str(e))
        return str(e), 500

@app.route('/batch_predict', methods=['GET', 'POST'])
def batch_predict():
    output_path = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return "Invalid file", 400
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        df = pd.read_csv(filepath)
        preds = model.predict(df.values).tolist()
        df['Predicted_Yield'] = preds
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], "predictions.csv")
        df.to_csv(output_path, index=False)
        logging.info("Batch prediction saved")
    return render_template('batch_predict.html', output_path=output_path, current_year=2025)

@app.route('/api_predict', methods=['GET', 'POST'])
def api_predict():
    if request.method == 'POST':
        data = request.get_json()
        values = [
            data.get('soil_n'),
            data.get('soil_p'),
            data.get('soil_k'),
            data.get('rainfall'),
            data.get('temp')
        ]
        pred = model.predict(np.array([values]))[0]
        return jsonify({"predicted_yield": pred})
    return render_template('api_predict.html', current_year=2025)

@app.route('/dashboard')
def dashboard():
    combined_vs_yield = [
        {
            "nitrogen": round(random.uniform(10,50),2),
            "phosphorus": round(random.uniform(5,40),2),
            "potassium": round(random.uniform(10,60),2),
            "rainfall": round(random.uniform(500,1500),2),
            "temperature": round(random.uniform(15,35),2),
            "yield_": round(random.uniform(2,8),2)
        } for _ in range(20)
    ]
    return render_template("dashboard.html", combined_vs_yield=combined_vs_yield, current_year=2025)

if __name__ == "__main__":
    app.run(debug=True)
