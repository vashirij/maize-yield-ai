import sys
import joblib
import pandas as pd
import requests

API_KEY = '4a5003fd6f81c1b15a3472d2ad89f92e'
DEFAULT_DISTRICT = 'Marondera'

# Coordinates for some districts - add more as needed
DISTRICT_COORDS = {
    'marondera': {'lat': -18.1867, 'lon': 31.5500},
    # Add other districts here
}


def get_weather_data(lat, lon):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url)
        data = response.json()
        if 'current' not in data:
            return None, f"Weather API error: {data}"
        current = data['current']
        temp = current.get('temp')
        humidity = current.get('humidity')
        rain = current.get('rain', {}).get('1h', 0)  # mm in last hour, fallback 0
        return {
            'Average Temperature': temp,
            'Average Relative Humidity': humidity,
            'Average Rain (mm)': rain
        }, None
    except Exception as e:
        return None, f"Error fetching weather data: {e}"


def fertilizer_irrigation_advice(soil_type, weather):
    advice = []

    # Base fertilizer recommendations for maize (kg/ha)
    fertilizer_recs = {
        'sandy': {'N': 120, 'P': 60, 'K': 60},
        'loamy sandy': {'N': 110, 'P': 55, 'K': 55},
        'loam': {'N': 100, 'P': 50, 'K': 50},
        'clay loam': {'N': 90, 'P': 60, 'K': 60},
        'clay': {'N': 80, 'P': 70, 'K': 70},
    }

    soil_key = soil_type.lower()
    fert = fertilizer_recs.get(soil_key, {'N': 100, 'P': 50, 'K': 50})  # default values

    # Irrigation water requirement in mm (approximate for maize growth period)
    # Maize needs about 500-800 mm total; subtract rainfall to get irrigation need.
    maize_total_water_mm = 650  # average value
    rain_mm = weather['Average Rain (mm)']
    irrigation_mm = max(maize_total_water_mm - rain_mm, 0)  # no negative irrigation

    # Convert irrigation mm to liters per hectare (1 mm = 10,000 liters per hectare)
    irrigation_liters_per_ha = irrigation_mm * 10000

    # Advisory messages
    if soil_key in ['sandy', 'loamy sandy']:
        advice.append("Sandy soils drain quickly; irrigate more frequently with smaller amounts.")
    elif soil_key in ['clay', 'clay loam']:
        advice.append("Clay soils hold water; irrigate less frequently to avoid waterlogging.")
    else:
        advice.append("Use balanced irrigation schedule for your soil type.")

    if irrigation_mm == 0:
        advice.append("Rainfall is sufficient; irrigation may not be needed currently.")
    else:
        advice.append(
            f"Estimated irrigation requirement: {irrigation_mm:.1f} mm (~{irrigation_liters_per_ha:.0f} liters per hectare).")

    advice.append(f"Recommended fertilizer application per hectare for {soil_type.title()} soil (Maize):")
    advice.append(f"  - Nitrogen (N): {fert['N']} kg/ha")
    advice.append(f"  - Phosphorus (P): {fert['P']} kg/ha")
    advice.append(f"  - Potassium (K): {fert['K']} kg/ha")

    return advice


def main():
    if len(sys.argv) != 5:
        print("Usage: python RF_predict.py <district> <crop> <soil> <area>")
        sys.exit(1)

    district = sys.argv[1].lower()
    crop = sys.argv[2].lower()
    soil = sys.argv[3].lower()
    try:
        area = float(sys.argv[4])
    except ValueError:
        print("Error: Area must be a number.")
        sys.exit(1)

    if district not in DISTRICT_COORDS:
        print(f"District '{district}' not found, using default '{DEFAULT_DISTRICT}'.")
        district = DEFAULT_DISTRICT.lower()

    coords = DISTRICT_COORDS[district]

    weather_data, error = get_weather_data(coords['lat'], coords['lon'])
    if error:
        print(error)
        weather_data = {
            'Average Temperature': 24.5,
            'Average Relative Humidity': 75.0,
            'Average Rain (mm)': 10.0
        }

    print(
        f"Weather for {district.title()}:\n- Temp: {weather_data['Average Temperature']} C\n- Humidity: {weather_data['Average Relative Humidity']}%\n- Rain: {weather_data['Average Rain (mm)']} mm")

    # Load model
    try:
        model = joblib.load('RF_Model.joblib')
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

    input_df = pd.DataFrame([{
        'Average Temperature': weather_data['Average Temperature'],
        'Average Relative Humidity': weather_data['Average Relative Humidity'],
        'Average Rain (mm)': weather_data['Average Rain (mm)']
    }])

    try:
        prediction = model.predict(input_df)
        predicted_yield_per_ha = prediction[0]
        total_yield = predicted_yield_per_ha * area
        print(f"Predicted Maize Yield per hectare: {predicted_yield_per_ha:.2f} tons/ha")
        print(f"Total Predicted Yield for {area} hectares: {total_yield:.2f} tons")
    except Exception as e:
        print(f"Error during prediction: {e}")
        sys.exit(1)

    advice = fertilizer_irrigation_advice(soil, weather_data)
    print("\nFertilizer and Irrigation Advisory:")
    for line in advice:
        print(f"- {line}")


if __name__ == "__main__":
    main()
