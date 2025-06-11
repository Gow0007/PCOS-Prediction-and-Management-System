# PCOS-Prediction-and-Management-System

A Flask-based web application that predicts Polycystic Ovary Syndrome (PCOS) risk using machine learning and provides cycle and mood tracking features. This tool helps women assess their PCOS risk and manage symptoms effectively.

## Key Features
- ✅ PCOS risk prediction with 90.79% accuracy
- 📅 Menstrual cycle tracking with period/ovulation predictions
- 😊 Mood and symptom tracker with personalized recommendations
- 📊 Interactive dashboard with historical data visualization
- 🏥 Educational resources about PCOS symptoms and management

## Project Highlights
  - Developed end-to-end machine learning pipeline from data cleaning to model deployment
  - Implemented user-friendly interface with comprehensive health tracking features
  - Achieved 90.79% prediction accuracy using Random Forest algorithm

## Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **ML**: Scikit-learn, Pandas, NumPy
- **Data**: Pickle for model serialization

## Installation & Usage

1. **Clone the repository**
```bash
git clone https://github.com/your-username/pcos-prediction.git
cd pcos-prediction

2.Create virtual environment (optional)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3.Install dependencies

pip install -r requirements.txt

4.Run the application

python app.py

5.Access the application

Open http://127.0.0.1:5000 in your browser

Project Structure

pcos-prediction/
├── static/            # CSS/JS files
├── templates/         # HTML templates
├── model.pkl          # Trained ML model
├── scaler.pkl         # Feature scaler
├── app.py             # Flask application
├── model.py           # Model training script
├── PCOS_data.csv      # Dataset
└── requirements.txt   # Dependencies


##Future Enhancements
Add user authentication for personalized dashboards

Implement data visualization charts for tracking history

Expand recommendation engine with nutrition/supplement advice

Deploy on cloud platform for public access
