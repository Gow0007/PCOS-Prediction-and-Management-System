from flask import Flask, request, render_template, redirect, url_for, session
import pickle
import numpy as np
from datetime import datetime, timedelta
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure secret key
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Add timedelta to template context
@app.context_processor
def inject_timedelta():
    return dict(timedelta=timedelta)

# Custom Jinja2 filter for datetime conversion
def to_datetime(value, format='%Y-%m-%d'):
    return datetime.strptime(value, format)

app.jinja_env.filters['to_datetime'] = to_datetime

# Load the model and scaler
try:
    model = pickle.load(open('model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    scaler = None

# Mood recommendations
MOOD_RECOMMENDATIONS = {
    'high': [
        "Listen to calming music",
        "Practice deep breathing exercises",
        "Take a warm bath",
        "Try gentle yoga",
        "Write in a journal"
    ],
    'medium': [
        "Go for a short walk",
        "Drink herbal tea",
        "Eat some dark chocolate",
        "Call a friend",
        "Do some light stretching"
    ],
    'low': [
        "Engage in your favorite hobby",
        "Watch a funny movie",
        "Dance to upbeat music",
        "Spend time in nature",
        "Practice gratitude"
    ]
}

@app.route("/")
def home():
    # Initialize session variables if they don't exist
    if 'cycle_data' not in session:
        session['cycle_data'] = []
    if 'mood_data' not in session:
        session['mood_data'] = []
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('index.html', scroll_to='about')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None:
        return render_template('index.html', 
                             prediction_text='Model not loaded. Please try again later.',
                             scroll_to='prediction-result')
    
    try:
        # Get all form data
        features = [
            float(request.form.get('Age', 0)),
            float(request.form.get('Weight', 0)),
            float(request.form.get('Height', 0)),
            float(request.form.get('BMI', 0)),
            float(request.form.get('PulseRate', 0)),
            float(request.form.get('RR', 0)),
            float(request.form.get('Hb', 0)),
            float(request.form.get('Cycle', 0)),
            float(request.form.get('MarriageStatus', 0)),
            float(request.form.get('Pregnant', 0)),
            float(request.form.get('NoOfAbortions', 0)),
            float(request.form.get('FSH', 0)),
            float(request.form.get('LH', 0)),
            float(request.form.get('FSH_LH_ratio', 0)),
            float(request.form.get('Hip', 0)),
            float(request.form.get('Waist', 0)),
            float(request.form.get('WaistHipRatio', 0)),
            float(request.form.get('TSH', 0)),
            float(request.form.get('AMH', 0)),
            float(request.form.get('PRL', 0)),
            float(request.form.get('VitD3', 0)),
            float(request.form.get('PRG', 0)),
            float(request.form.get('RBS', 0)),
            float(request.form.get('WeightGain', 0)),
            float(request.form.get('HairGrowth', 0)),
            float(request.form.get('SkinDarkening', 0)),
            float(request.form.get('HairLoss', 0)),
            float(request.form.get('Pimples', 0)),
            float(request.form.get('FastFood', 0)),
            float(request.form.get('RegExercise', 0)),
            float(request.form.get('BPSystolic', 0)),
            float(request.form.get('BPDiastolic', 0)),
            float(request.form.get('FollicleNoL', 0)),
            float(request.form.get('FollicleNoR', 0)),
            float(request.form.get('AvgFSizeL', 0)),
            float(request.form.get('AvgFSizeR', 0)),
            float(request.form.get('Endometrium', 0))
        ]
        
        # Select only the features used in the model (29 features)
        selected_features = [
            features[0],  # Age
            features[1],  # Weight
            features[2],  # Height
            features[3],  # BMI
            features[4],  # PulseRate
            features[5],  # RR
            features[6],  # Hb
            features[7],  # Cycle
            features[10], # NoOfAbortions
            features[11], # FSH
            features[12], # LH
            features[13], # FSH_LH_ratio
            features[16], # WaistHipRatio
            features[17], # TSH
            features[18], # AMH
            features[19], # PRL
            features[20], # VitD3
            features[21], # PRG
            features[22], # RBS
            features[23], # WeightGain
            features[24], # HairGrowth
            features[25], # SkinDarkening
            features[26], # HairLoss
            features[27], # Pimples
            features[28], # FastFood
            features[29], # RegExercise
            features[30], # BPSystolic
            features[31], # BPDiastolic
            features[32] + features[33]  # Follicle_count (L + R)
        ]
        
        final_features = [np.array(selected_features)]
        
        # Scale features
        final_features = scaler.transform(final_features)
        
        # Make prediction
        prediction = model.predict(final_features)
        
        if prediction == 1:
            prediction_text = 'The model suggests possible PCOS with an accuracy of 90.79%. Please consult a healthcare professional for proper diagnosis.'
            result_class = 'positive'
        else:
            prediction_text = 'The model suggests no signs of PCOS with an accuracy of 90.79%. However, consult a doctor if you have concerns.'
            result_class = 'negative'
            
    except Exception as e:
        print(f"Prediction error: {e}")
        prediction_text = 'Error processing your request. Please check your inputs and try again.'
        result_class = 'error'
    
    return render_template('index.html', 
                         prediction_text=prediction_text,
                         result_class=result_class,
                         scroll_to='prediction-result')

@app.route('/track_cycle', methods=['POST'])
def track_cycle():
    cycle_date = request.form.get('cycle_date')
    notes = request.form.get('cycle_notes', '')
    cycle_message = ""
    
    if cycle_date:
        try:
            # Get existing data or initialize
            cycle_data = session.get('cycle_data', [])
            
            # Add new entry
            cycle_data.append({
                'date': cycle_date,
                'notes': notes
            })
            
            # Update session
            session['cycle_data'] = cycle_data
            
            # Calculate next predicted cycle dates (assuming 28-day cycle)
            last_date = datetime.strptime(cycle_date, '%Y-%m-%d')
            next_cycle = last_date + timedelta(days=28)
            next_ovulation = last_date + timedelta(days=14)
            
            cycle_message = f"Cycle tracked! Next period around {next_cycle.strftime('%B %d, %Y')}, ovulation around {next_ovulation.strftime('%B %d, %Y')}."
        except Exception as e:
            print(f"Cycle tracking error: {e}")
            cycle_message = "Error processing your cycle data. Please try again."
    else:
        cycle_message = "Please select a valid date."
    
    return render_template('index.html', 
                         cycle_message=cycle_message, 
                         scroll_to='cycle-tracker',
                         last_date=cycle_date if cycle_date else None)

@app.route('/track_mood', methods=['POST'])
def track_mood():
    mood_level = request.form.get('mood_level')
    pain_level = request.form.get('pain_level')
    notes = request.form.get('mood_notes', '')
    mood_message = ""
    recommendations = []
    
    if mood_level and pain_level:
        try:
            # Get existing data or initialize
            mood_data = session.get('mood_data', [])
            
            # Add new entry
            mood_data.append({
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'mood': mood_level,
                'pain': pain_level,
                'notes': notes
            })
            
            # Update session
            session['mood_data'] = mood_data
            
            # Get recommendations based on mood level
            recommendations = MOOD_RECOMMENDATIONS.get(mood_level, [])
            if pain_level in ['medium', 'high']:
                recommendations.extend([
                    "Consider a heating pad", 
                    "Take prescribed pain medication", 
                    "Rest and relax"
                ])
            
            mood_message = "Mood and symptoms tracked successfully!"
        except Exception as e:
            print(f"Mood tracking error: {e}")
            mood_message = "Error processing your mood data. Please try again."
    else:
        mood_message = "Please select both mood and pain levels."
    return render_template('index.html', 
                         mood_message=mood_message,
                         recommendations=recommendations,
                         scroll_to='mood-tracker')

if __name__ == "__main__":
    app.run(debug=True)