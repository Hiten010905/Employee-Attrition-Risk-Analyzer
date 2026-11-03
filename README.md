# Employee Attrition Prediction

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Latest-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

This project predicts employee attrition using machine learning. The application helps organizations identify employees who are likely to leave, enabling proactive retention strategies. The predictive model is built using Logistic Regression and is deployed as an interactive web application using Streamlit.

## Features

- **Data Preprocessing**: Handles outliers, manages skewed features, performs feature engineering and transformation
- **Feature Engineering**: Creates meaningful features like satisfaction product, age groups, and tenure categories
- **Model Building**: Uses Logistic Regression with optimized hyperparameters through GridSearchCV
- **Threshold Optimization**: Implements custom probability threshold to maximize F1-score
- **Interactive Web App**: User-friendly interface to input employee information and get attrition predictions
- **Visualization**: Displays key factors influencing attrition risk

## Dataset

The model is trained on the IBM HR Analytics Employee Attrition dataset (`WA_Fn-UseC_-HR-Employee-Attrition.csv`), which includes various features like:

- Demographics (Age, Gender, MaritalStatus)
- Work-related metrics (JobRole, JobLevel, JobSatisfaction)
- Compensation details (MonthlyIncome, StockOptionLevel)
- Work-life balance indicators (WorkLifeBalance, OverTime)
- Career development metrics (YearsInCurrentRole, YearsSinceLastPromotion)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/employee-attrition-prediction.git
cd employee-attrition-prediction

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## Usage

### Running the Streamlit Web App

```bash
streamlit run app.py
```

This will launch the web application in your default browser where you can:
1. Enter employee information through the user interface
2. Get predictions on attrition probability
3. View key factors influencing the prediction

### Using the Model Programmatically

```python
import pandas as pd
import joblib

# Load the model
model = joblib.load('attrition_model.pkl')

# Prepare input data (example)
employee_data = pd.DataFrame({
    'Age': [35],
    'BusinessTravel': ['Travel_Rarely'],
    'DailyRate': [800],
    # Add all required features...
})

# Add engineered features
# (See logistic_reg_train.pdf for required feature engineering steps)

# Make prediction
prediction = model.predict(employee_data)
probability = model.predict_proba(employee_data)[:, 1]

print(f"Attrition Prediction: {'Yes' if prediction[0] == 1 else 'No'}")
print(f"Probability of Attrition: {probability[0]:.2f}")
```

## Model Performance

The logistic regression model achieves:
- F1-score: 0.64 (for positive class at optimal threshold)
- ROC-AUC score: 0.86
- Accuracy: 0.88

Key predictive features include:
- Work-life balance and overtime
- Monthly income
- Business travel frequency
- Job involvement
- Environmental satisfaction

## File Structure

```
employee-attrition-prediction/
├── app.py                        # Streamlit web application
├── attrition_model.pkl           # Trained model
├── WA_Fn-UseC_-HR-Employee-Attrition.csv  # Dataset
├── logistic_reg_train.ipynb      # Model training notebook
├── requirements.txt              # Required packages
├── README.md                     # Project documentation
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- IBM for providing the HR Analytics dataset
- Scikit-learn community for machine learning tools
- Streamlit team for the interactive web app framework
