import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle

# Load the dataset
df = pd.read_csv('PCOS_data.csv')

# Data cleaning
df = df.drop(['Sl. No', 'Patient File No.', 'Marraige Status (Yrs)', 'Blood Group'], axis=1)

# Feature engineering
df['Follicle_count'] = df['Follicle No. (L)'] + df['Follicle No. (R)']
df = df.drop(['Follicle No. (L)', 'Follicle No. (R)'], axis=1)

# Encoding categorical variables
df["Cycle(R/I)"].replace({2: 0, 4: 1, 5: 0}, inplace=True)

# Renaming columns for clarity
df.rename(columns={
    'PCOS (Y/N)': 'PCOS',
    'Age (yrs)': 'Age',
    'Weight (Kg)': 'Weight',
    'Height(Cm)': 'Height',
    'Pulse rate(bpm)': 'PulseRate',
    'RR (breaths/min)': 'RR',
    'Pregnant(Y/N)': 'Pregnant',
    'No. of aborptions': 'Abortions',
    'FSH(mIU/mL)': 'FSH',
    'TSH (mIU/L)': 'TSH',
    'LH(mIU/mL)': 'LH',
    'AMH(ng/mL)': 'AMH',
    'PRL(ng/mL)': 'PRL',
    'Vit D3 (ng/mL)': 'VitD3',
    'PRG(ng/mL)': 'PRG',
    'RBS(mg/dl)': 'RBS',
    'Weight gain(Y/N)': 'Weight_gain',
    'hair growth(Y/N)': 'hair_growth',
    'Skin darkening (Y/N)': 'Skin_darkening',
    'Hair loss(Y/N)': 'Hair_loss',
    'FSH/LH': 'FSH_LH_ratio',
    'Pimples(Y/N)': 'Pimples',
    'Fast food (Y/N)': 'Fast_food',
    'Reg.Exercise(Y/N)': 'Reg_exercise',
    'BP _Systolic (mmHg)': 'BP_systolic',
    'BP _Diastolic (mmHg)': 'BP_diastolic',
    'Waist:Hip Ratio': 'W_H_ratio',
    'Hip(inch)': 'Hip',
    'Waist(inch)': 'Waist',
    'Cycle length(days)': 'Cycle_length',
    'Avg. F size (L) (mm)': 'Avg_F_size_L',
    'Avg. F size (R) (mm)': 'Avg_F_size_R',
    'Endometrium (mm)': 'Endometrium'
}, inplace=True)

# Select the features used in the model
features = [
    'Age', 'Weight', 'Height', 'BMI', 'PulseRate', 'RR', 'Hb(g/dl)', 'Cycle(R/I)',
    'Abortions', 'FSH', 'LH', 'FSH_LH_ratio', 'W_H_ratio', 'TSH', 'AMH', 'PRL',
    'VitD3', 'PRG', 'RBS', 'Weight_gain', 'hair_growth', 'Skin_darkening',
    'Hair_loss', 'Pimples', 'Fast_food', 'Reg_exercise', 'BP_systolic',
    'BP_diastolic', 'Follicle_count'
]

X = df[features]
y = df['PCOS']

# Split data into train and test sets
train_X, test_X, train_y, test_y = train_test_split(
    X, y, test_size=0.3, random_state=0, stratify=y
)

# Feature scaling
sc = StandardScaler()
train_X = sc.fit_transform(train_X)
test_X = sc.transform(test_X)

# Train Random Forest model
model_rfc = RandomForestClassifier(n_estimators=110, random_state=0)
model_rfc.fit(train_X, train_y)

# Evaluate model
predictions = model_rfc.predict(test_X)
accuracy = metrics.accuracy_score(predictions, test_y)
print(f'The accuracy of the Random Forest model is {accuracy*100:.2f}%')

# Save the model and scaler
pickle.dump(model_rfc, open('model.pkl', 'wb'))
pickle.dump(sc, open('scaler.pkl', 'wb'))