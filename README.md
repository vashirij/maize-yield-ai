
```markdown
Maize Yield Prediction App

A Flask-based web application that predicts maize yield using a machine learning model.  
This project demonstrates skills in backend API design, data validation, batch processing, data visualization, and containerized deployment.

Features

- Single Prediction: Enter soil nutrients, rainfall, and temperature to predict yield.
- Batch Prediction: Upload a CSV file for bulk predictions.
- REST API Endpoint: JSON-based predictions for programmatic use.
- Data Visualization Dashboard: View trends between environmental factors and predicted yield.
- Input Validation: Ensures clean and safe data for the model.
- Logging: Tracks predictions and errors for debugging.
- Dockerized: Easy to run anywhere.
- Ready for GitHub Portfolio: Clean structure, requirements.txt, and Dockerfile included.

📂 Project Structure


maize\_prediction\_app/
│
├── app.py                  # Main Flask application
├── config.py               # App configuration
├── models/
│   └── maize\_model.pkl     # Pre-trained model (dummy/demo)
├── static/
│   ├── style.css           # App styling
│   └── charts.js           # (Optional) for interactive charts
├── templates/
│   ├── index.html          # Main form & upload page
│   └── dashboard.html      # Data visualization page
├── utils/
│   ├── validation.py       # Input validation helpers
│   └── visualization.py    # Matplotlib plotting functions
├── uploads/                # Uploaded CSV files & batch predictions
├── requirements.txt        # Python dependencies
├── Dockerfile              # Containerization
└── README.md               # Project documentation

````

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/maize-yield-prediction.git
cd maize-yield-prediction
````

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python app.py
```

App will be live at **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**.

---

## 🐳 Docker Deployment

Build and run with Docker:

```bash
docker build -t maize-yield-app .
docker run -p 5000:5000 maize-yield-app
```

---

## 📊 API Usage

### **Endpoint**

`POST /api/predict`

### **Request Example**

```json
{
  "soil_n": 100,
  "soil_p": 40,
  "soil_k": 50,
  "rainfall": 120,
  "temp": 25
}
```

### **Response**

```json
{
  "predicted_yield": 4.53
}
```

---

## 📂 Batch Prediction

1. Prepare a CSV file with **exactly these columns** (no headers required by default model):

```
soil_nitrogen,soil_phosphorus,soil_potassium,rainfall,temperature
100,40,50,120,25
90,35,60,140,27
```

2. Upload through the web form on `/`.
3. Download the generated predictions CSV from the `uploads/` folder.

---

## 📈 Dashboard

The `/dashboard` route displays scatter plots of environmental factors vs predicted yields.
Plots are generated dynamically using **Matplotlib**.

---

## 🔧 Technologies Used

* **Backend**: Flask (Python)
* **ML Model**: scikit-learn (dummy regression model for demo)
* **Data Processing**: NumPy, Pandas
* **Visualization**: Matplotlib
* **Containerization**: Docker
* **Deployment Ready**: Requirements.txt, config file, logging

---

## 📜 License

This project is released under the MIT License.

---

## ✨ Author

**James Vashiri** – *Data & Software Developer*
 [grinefalcon2@gmail.com.com](mailto:your.email@example.com)
