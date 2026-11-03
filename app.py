import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Employee Attrition Risk Evaluator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;0,800;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --font-serif: 'Playfair Display', Georgia, serif;
        --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        
        --bg-beige-darker: #E2D9C5;
        --bg-beige-card: #FAF6EE;
        --border-beige: #C5B89F;
        
        --text-dark: #0C1A13;
        --text-muted: #2E4E3C;
        --accent-teal: #0F766E;
        --accent-emerald: #059669;
        
        --risk-high-bg: #FEE2E2;
        --risk-high-border: #EF4444;
        --risk-low-bg: #D1FAE5;
        --risk-low-border: #10B981;
        
        --radius-lg: 16px;
        --radius-md: 10px;
    }

    /* App Canvas and Sidebar Base Background */
    .stApp, section[data-testid="stSidebar"] {
        background-color: var(--bg-beige-darker) !important;
        font-family: var(--font-sans);
        color: var(--text-dark) !important;
    }

    /* Headings Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-serif);
        font-weight: 700;
        letter-spacing: -0.01em;
        color: var(--text-dark) !important;
    }

    /* Header Banner */
    .hero-container {
        background-color: var(--bg-beige-card);
        border: 1.5px solid var(--border-beige);
        border-radius: var(--radius-lg);
        padding: 2.2rem 2.5rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px rgba(12, 26, 19, 0.06);
    }

    .hero-tag {
        display: inline-block;
        font-family: var(--font-sans);
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-dark);
        background-color: rgba(12, 26, 19, 0.08);
        padding: 4px 14px;
        border-radius: 20px;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(12, 26, 19, 0.18);
    }

    .hero-title {
        font-family: var(--font-serif);
        font-size: 2.3rem;
        font-weight: 700;
        color: var(--text-dark) !important;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.02rem;
        color: var(--text-dark) !important;
        line-height: 1.6;
        max-width: 820px;
        margin: 0;
    }

    /* Section Headers */
    .section-header {
        font-family: var(--font-serif);
        font-size: 1.38rem;
        font-weight: 700;
        color: var(--text-dark) !important;
        margin-top: 1.4rem;
        margin-bottom: 0.85rem;
        padding-bottom: 6px;
        border-bottom: 2px solid var(--border-beige);
    }

    /* Card Containers (Main & Sidebar) */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stBlock"] {
        background-color: var(--bg-beige-card) !important;
        border: 1.5px solid var(--border-beige) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.35rem !important;
        color: var(--text-dark) !important;
        box-shadow: 0 4px 14px rgba(12, 26, 19, 0.05);
    }

    /* FORCE ALL TEXT IN CARDS AND SIDEBAR TO BE DEEP DARK CHARCOAL */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stBlock"] p,
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stBlock"] span,
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stBlock"] div,
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stBlock"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] caption {
        color: var(--text-dark) !important;
    }

    /* Widget Labels (Age, Gender, Marital Status, Sliders, etc) */
    [data-testid="stWidgetLabel"] label, 
    [data-testid="stWidgetLabel"] p,
    .stSlider label, .stSelectbox label {
        color: var(--text-dark) !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.01em;
    }

    /* Selectbox Fields Styling */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: var(--text-dark) !important;
        border: 1.5px solid #A89B80 !important;
        border-radius: var(--radius-md) !important;
    }

    .stSelectbox div[data-baseweb="select"] span {
        color: var(--text-dark) !important;
        font-weight: 600 !important;
    }

    .stSelectbox svg {
        fill: var(--text-dark) !important;
    }

    /* Slider Values & Markings */
    .stSlider div[data-testid="stMarkdownContainer"] p,
    .stSlider [data-baseweb="slider"] {
        color: var(--text-dark) !important;
        font-weight: 700 !important;
    }

    /* Help Icon SVG Tooltips */
    [data-testid="stTooltipHoverTarget"] svg {
        fill: var(--text-muted) !important;
    }

    /* Primary Action Button */
    .stButton > button {
        width: 100%;
        background-color: var(--text-dark) !important;
        color: #FAF6EE !important;
        font-family: var(--font-serif);
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.85rem 1.8rem;
        border-radius: var(--radius-md);
        border: 1.5px solid var(--text-dark) !important;
        box-shadow: 0 6px 16px rgba(12, 26, 19, 0.18);
        cursor: pointer;
        transition: all 0.25s ease;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    .stButton > button:hover {
        background-color: var(--accent-teal) !important;
        color: #FFFFFF !important;
        border-color: var(--accent-teal) !important;
        transform: translateY(-2px);
    }

    /* Risk Banners */
    .risk-banner {
        border-radius: var(--radius-lg);
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        border: 1.5px solid;
    }

    .risk-banner-high {
        background-color: var(--risk-high-bg);
        border-color: var(--risk-high-border);
    }

    .risk-banner-low {
        background-color: var(--risk-low-bg);
        border-color: var(--risk-low-border);
    }

    .risk-tag {
        display: inline-block;
        font-family: var(--font-sans);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 3px 10px;
        border-radius: 4px;
        margin-bottom: 0.4rem;
    }

    .risk-tag-high {
        background-color: var(--risk-high-border);
        color: #FFFFFF;
    }

    .risk-tag-low {
        background-color: var(--risk-low-border);
        color: #FFFFFF;
    }

    .risk-title {
        font-family: var(--font-serif);
        font-size: 1.35rem;
        font-weight: 700;
        margin: 0;
    }

    .risk-title-high { color: #991B1B !important; }
    .risk-title-low { color: #065F46 !important; }

    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-family: var(--font-serif);
        font-weight: 700;
        color: var(--accent-teal) !important;
        font-size: 2.3rem !important;
    }

    [data-testid="stMetricLabel"] {
        font-weight: 700;
        color: var(--text-muted) !important;
    }

    /* Expander Styling */
    .stExpander {
        background-color: var(--bg-beige-card) !important;
        border: 1.5px solid var(--border-beige) !important;
        border-radius: var(--radius-md) !important;
    }

    .stExpander summary,
    .stExpander summary *,
    .stExpander summary span,
    .stExpander summary p {
        color: var(--text-dark) !important;
        font-weight: 700 !important;
    }

    /* Sidebar Background & Borders */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-beige-darker) !important;
        border-right: 1.5px solid var(--border-beige);
    }

    section[data-testid="stSidebar"] .section-header {
        color: var(--text-dark) !important;
        border-bottom-color: var(--border-beige);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Header Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">HR Talent Intelligence</div>
    <div class="hero-title">Employee Attrition Risk Evaluator</div>
    <div class="hero-subtitle">
        Evaluate individual retention risk probabilities and key driver contributions using machine learning analytics.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Model Loading Pipeline
# ---------------------------------------------------------
MODEL_PATH = 'attrition_model.pkl'

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception as e:
            st.error(f"Error loading model from '{MODEL_PATH}': {e}")
            return None
    else:
        st.error(f"Model file '{MODEL_PATH}' not found! Please train the model first.")
        return None

model = load_model()

# Feature labels stripped of emojis with high-contrast text formatting
FEATURE_LABELS = {
    'num__Age': "Age",
    'num__DailyRate': "Daily Rate",
    'num__Education': "Education Level",
    'num__EnvironmentSatisfaction': "Environment Satisfaction",
    'num__HourlyRate': "Hourly Rate",
    'num__JobInvolvement': "Job Involvement",
    'num__JobSatisfaction': "Job Satisfaction",
    'num__MonthlyRate': "Monthly Rate",
    'num__RelationshipSatisfaction': "Relationship Satisfaction",
    'num__WorkLifeBalance': "Work-Life Balance",
    'num__LogMonthlyIncome': "Monthly Income",
    'num__LogNumCompaniesWorked': "Num Companies Worked",
    'num__LogStockOptionLevel': "Stock Option Level",
    'num__LogTrainingTimesLastYear': "Trainings Last Year",
    'num__LogYearsAtCompany': "Years at Company",
    'num__LogYearsInCurrentRole': "Years in Current Role",
    'num__LogYearsSinceLastPromotion': "Years Since Promotion",
    'num__LogIncomePerWorkingYear': "Income per Working Year",
    'num__LogDistanceFromHome': "Distance from Home",
    'num__LogPercentSalaryHike': "Percent Salary Hike",
    'num__SatisfactionProduct': "Overall Satisfaction Combo",
    'num__PromotionSatisfaction': "Promotion & Satisfaction",
    'num__OverTimeWorkLife': "Overtime & Work-Life Balance",
    'cat__Department_Research & Development': "Dept: R&D",
    'cat__Department_Sales': "Dept: Sales",
    'cat__EducationField_Life Sciences': "Field: Life Sciences",
    'cat__EducationField_Marketing': "Field: Marketing",
    'cat__EducationField_Medical': "Field: Medical",
    'cat__EducationField_Other': "Field: Other",
    'cat__EducationField_Technical Degree': "Field: Technical Degree",
    'cat__Gender_Male': "Gender: Male",
    'cat__JobRole_Human Resources': "Role: Human Resources",
    'cat__JobRole_Laboratory Technician': "Role: Lab Technician",
    'cat__JobRole_Manager': "Role: Manager",
    'cat__JobRole_Manufacturing Director': "Role: Mfg Director",
    'cat__JobRole_Research Director': "Role: Research Director",
    'cat__JobRole_Research Scientist': "Role: Research Scientist",
    'cat__JobRole_Sales Executive': "Role: Sales Executive",
    'cat__JobRole_Sales Representative': "Role: Sales Rep",
    'cat__MaritalStatus_Married': "Status: Married",
    'cat__MaritalStatus_Single': "Status: Single",
    'cat__OverTime_Yes': "Works Overtime",
    'ord__BusinessTravel': "Business Travel Frequency"
}

# ---------------------------------------------------------
# Feature Input Section
# ---------------------------------------------------------
def create_feature_input():
    col1, col2, col3 = st.columns(3)
    
    input_data = {}
    
    with col1:
        st.markdown('<div class="section-header">Personal Profile</div>', unsafe_allow_html=True)
        with st.container(border=True):
            input_data['Age'] = st.slider("Age", min_value=18, max_value=60, value=35, step=1, 
                                      help="Age of employee")
            
            input_data['Gender'] = st.selectbox("Gender", options=["Male", "Female"], 
                                            help="Gender of employee")
            
            input_data['MaritalStatus'] = st.selectbox("Marital Status", 
                                                   options=["Single", "Married", "Divorced"], 
                                                   help="Marital status of employee")
            
            input_data['DistanceFromHome'] = st.slider("Distance From Home (miles)", min_value=1, max_value=30, 
                                                   value=10, step=1, 
                                                   help="Distance from home in miles/km")
            
            input_data['NumCompaniesWorked'] = st.slider("Previous Companies Worked", 
                                                     min_value=0, max_value=10, value=2, step=1,
                                                     help="Number of companies worked at before")
            
    with col2:
        st.markdown('<div class="section-header">Job & Role</div>', unsafe_allow_html=True)
        with st.container(border=True):
            input_data['Department'] = st.selectbox("Department", 
                                                options=["Research & Development", "Sales", "Human Resources"], 
                                                help="Employee's department")
            
            input_data['JobRole'] = st.selectbox("Job Role", 
                                             options=["Sales Executive", "Research Scientist", 
                                                     "Laboratory Technician", "Manufacturing Director", 
                                                     "Healthcare Representative", "Manager", 
                                                     "Sales Representative", "Research Director", 
                                                     "Human Resources"], 
                                             help="Employee's job role")
            
            input_data['BusinessTravel'] = st.selectbox("Business Travel", 
                                                    options=["Non-Travel", "Travel_Rarely", "Travel_Frequently"], 
                                                    help="Frequency of business travel")
            
            input_data['OverTime'] = st.selectbox("Works Overtime?", 
                                              options=["No", "Yes"], 
                                              help="Does the employee work overtime?")
            
            input_data['YearsAtCompany'] = st.slider("Years at Company", 
                                                 min_value=0, max_value=40, value=5, step=1, 
                                                 help="Years at the company")
            
            input_data['YearsInCurrentRole'] = st.slider("Years in Current Role", 
                                                     min_value=0, max_value=20, value=3, step=1, 
                                                     help="Years in current role")
            
            input_data['YearsSinceLastPromotion'] = st.slider("Years Since Promotion", 
                                                           min_value=0, max_value=15, value=1, step=1, 
                                                           help="Years since last promotion")
            
    with col3:
        st.markdown('<div class="section-header">Compensation & Education</div>', unsafe_allow_html=True)
        with st.container(border=True):
            input_data['Education'] = st.slider("Education Level", 
                                            min_value=1, max_value=5, value=3, step=1, 
                                            help="1=Below College, 2=College, 3=Bachelor, 4=Master, 5=Doctor")
            
            input_data['EducationField'] = st.selectbox("Education Field", 
                                                    options=["Life Sciences", "Medical", "Marketing", 
                                                            "Technical Degree", "Human Resources", "Other"], 
                                                    help="Field of education")
            
            input_data['MonthlyIncome'] = st.slider("Monthly Income (Rs)", 
                                                min_value=1000, max_value=2000000, value=6000, step=500, 
                                                help="Monthly income in Ruppees")
            
            input_data['DailyRate'] = st.slider("Daily Rate (Rs)", 
                                            min_value=100, max_value=15000, value=800, step=50, 
                                            help="Daily rate in Ruppees")
            
            input_data['HourlyRate'] = st.slider("Hourly Rate (Rs)", 
                                             min_value=30, max_value=1000, value=65, step=5, 
                                             help="Hourly rate in Ruppees")
            
            input_data['MonthlyRate'] = st.slider("Monthly Rate (Rs)", 
                                              min_value=5000, max_value=25000, value=15000, step=1000, 
                                              help="Monthly rate in Ruppees")
            
            input_data['PercentSalaryHike'] = st.slider("Percent Salary Hike (%)", 
                                                    min_value=10, max_value=25, value=15, step=1, 
                                                    help="Percentage of last salary hike")
            
            input_data['StockOptionLevel'] = st.slider("Stock Option Level", 
                                                   min_value=0, max_value=3, value=1, step=1, 
                                                   help="Stock option level (0-3)")
            
            input_data['TrainingTimesLastYear'] = st.slider("Trainings Last Year", 
                                                        min_value=0, max_value=6, value=3, step=1, 
                                                        help="Number of trainings last year")
    
    st.markdown('<div class="section-header">Satisfaction & Work Dynamics</div>', unsafe_allow_html=True)
    with st.container(border=True):
        col_sat1, col_sat2, col_sat3, col_sat4, col_sat5 = st.columns(5)
        
        with col_sat1:
            input_data['JobSatisfaction'] = st.slider("Job Satisfaction", 
                                                  min_value=1, max_value=4, value=3, step=1, 
                                                  help="Job satisfaction level (1-4)")
        
        with col_sat2:
            input_data['EnvironmentSatisfaction'] = st.slider("Env Satisfaction", 
                                                          min_value=1, max_value=4, value=3, step=1, 
                                                          help="Environment satisfaction level (1-4)")
        
        with col_sat3:
            input_data['WorkLifeBalance'] = st.slider("Work Life Balance", 
                                                  min_value=1, max_value=4, value=3, step=1, 
                                                  help="Work life balance rating (1-4)")
        
        with col_sat4:
            input_data['RelationshipSatisfaction'] = st.slider("Relationship Sat", 
                                                           min_value=1, max_value=4, value=3, step=1, 
                                                           help="Relationship satisfaction level (1-4)")
        
        with col_sat5:
            input_data['JobInvolvement'] = st.slider("Job Involvement", 
                                                 min_value=1, max_value=4, value=3, step=1, 
                                                 help="Job involvement level (1-4)")
    
    return input_data

user_inputs = create_feature_input()

submit_button = st.button("Evaluate Attrition Risk")

# ---------------------------------------------------------
# Preprocessing & Model Prediction
# ---------------------------------------------------------
def preprocess_input(user_data):
    input_df = pd.DataFrame([user_data])
    
    total_years = user_data['YearsAtCompany'] + 1 
    input_df['IncomePerWorkingYear'] = user_data['MonthlyIncome'] / total_years
    
    skewed_features = ['MonthlyIncome', 'NumCompaniesWorked', 'StockOptionLevel', 
                      'TrainingTimesLastYear', 'YearsAtCompany', 'YearsInCurrentRole',
                      'YearsSinceLastPromotion', 'IncomePerWorkingYear', 'DistanceFromHome', 
                      'PercentSalaryHike']
    
    for col in skewed_features:
        input_df[f'Log{col}'] = np.log1p(input_df[col])
    
    input_df['SatisfactionProduct'] = input_df['JobSatisfaction'] * input_df['WorkLifeBalance']
    input_df['PromotionSatisfaction'] = input_df['LogYearsSinceLastPromotion'] * input_df['JobSatisfaction']
    input_df['OverTimeWorkLife'] = input_df['OverTime'].map({'Yes': 1, 'No': 0}) * input_df['WorkLifeBalance']
    
    input_df['AgeGroup'] = pd.cut(input_df['Age'], bins=[18, 30, 40, 50, 60], 
                                 labels=['Young', 'Early-Mid', 'Late-Mid', 'Senior'])
    input_df['TenureGroup'] = pd.cut(input_df['YearsAtCompany'], bins=[0, 2, 5, 10, 40], 
                                    labels=['New', 'Developing', 'Experienced', 'Veteran'])
    
    return input_df

def predict_attrition(processed_df):
    if model is not None:
        try:
            probabilities = model.predict_proba(processed_df)
            probability_yes = probabilities[0][1]
            
            prediction = model.predict(processed_df)[0]
            
            optimal_threshold = 0.535
            custom_prediction = 1 if probability_yes >= optimal_threshold else 0
            
            return prediction, probability_yes, custom_prediction
        except Exception as e:
            st.error(f"Prediction error: {e}")
            return None, None, None
    return None, None, None

def get_top_contributions(processed_df, top_n=5):
    if model is None:
        return pd.DataFrame()
    try:
        clf = model.named_steps['classifier']
        prep = model.named_steps['preprocessor']
        
        X_trans = prep.transform(processed_df)[0]
        feat_names = prep.get_feature_names_out()
        coefs = clf.coef_[0]
        
        contribs = X_trans * coefs
        
        factors = []
        for fname, val, coef, contrib in zip(feat_names, X_trans, coefs, contribs):
            label = FEATURE_LABELS.get(fname, fname.split('__')[-1])
            direction = "increases risk" if contrib > 0 else "decreases risk"
            factors.append({
                'factor': label,
                'impact': abs(contrib),
                'direction': direction,
                'contrib': contrib
            })
        df_factors = pd.DataFrame(factors)
        df_factors = df_factors.sort_values(by='impact', ascending=False).head(top_n)
        return df_factors
    except Exception as e:
        st.warning(f"Could not calculate feature contributions: {e}")
        return pd.DataFrame()

# ---------------------------------------------------------
# Output Section
# ---------------------------------------------------------
if submit_button:
    with st.spinner('Calculating risk metrics...'):
        processed_input = preprocess_input(user_inputs)
        prediction, probability, custom_prediction = predict_attrition(processed_input)
        
        if probability is not None:
            st.markdown('<div class="section-header">Predictive Analysis Results</div>', unsafe_allow_html=True)
            
            res_col1, res_col2 = st.columns([1, 1])
            
            with res_col1:
                if custom_prediction == 1:
                    st.markdown("""
                    <div class="risk-banner risk-banner-high">
                        <span class="risk-tag risk-tag-high">High Attrition Risk</span>
                        <div class="risk-title risk-title-high">Elevated Departure Risk</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="risk-banner risk-banner-low">
                        <span class="risk-tag risk-tag-low">Low Attrition Risk</span>
                        <div class="risk-title risk-title-low">Stable Retention Outlook</div>
                    </div>
                    """, unsafe_allow_html=True)

                with st.container(border=True):
                    st.metric("Calculated Probability of Departure", f"{probability:.1%}")
                    
                    if probability < 0.2:
                        risk_level = "Very Low Risk"
                        suggestion = "Employee demonstrates high stability. Maintain standard growth feedback cycles."
                    elif probability < 0.4:
                        risk_level = "Low Risk"
                        suggestion = "Overall attrition risk remains low. Continue periodic performance alignment."
                    elif probability < 0.6:
                        risk_level = "Moderate Risk"
                        suggestion = "Subtle risk factors detected. Review compensation alignment, workload balance, or career progression."
                    elif probability < 0.8:
                        risk_level = "High Risk"
                        suggestion = "Proactive retention strategy recommended. Conduct structured 1-on-1 session to address key concerns."
                    else:
                        risk_level = "Critical Risk"
                        suggestion = "Immediate intervention required. High probability of departure; consider targeted retention measures."
                    
                    st.markdown(f"<span style='color:#0C1A13; font-weight:700;'>Risk Level Tier:</span> <span style='color:#0F766E; font-weight:700;'>{risk_level}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#0C1A13; font-weight:700;'>Strategic Guidance:</span> <span style='color:#2E4E3C;'>{suggestion}</span>", unsafe_allow_html=True)
            
            with res_col2:
                with st.container(border=True):
                    # Styled Plotly Gauge Chart for Light Cream Background
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = probability * 100,
                        number = {'suffix': "%", 'font': {'size': 36, 'color': "#0F766E", 'family': "Playfair Display"}},
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Attrition Probability Index", 'font': {'size': 17, 'color': "#0C1A13", 'family': "Playfair Display"}},
                        gauge = {
                            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#0C1A13", 'tickfont': {'color': "#0C1A13", 'size': 12}},
                            'bar': {'color': "#0F766E", 'thickness': 0.3},
                            'bgcolor': "#FAF6EE",
                            'borderwidth': 1,
                            'bordercolor': "#C5B89F",
                            'steps': [
                                {'range': [0, 20], 'color': '#D1FAE5'},
                                {'range': [20, 40], 'color': '#A7F3D0'},
                                {'range': [40, 60], 'color': '#FEF3C7'},
                                {'range': [60, 80], 'color': '#FDE68A'},
                                {'range': [80, 100], 'color': '#FCA5A5'}
                            ],
                            'threshold': {
                                'line': {'color': "#EF4444", 'width': 3},
                                'thickness': 0.8,
                                'value': 53.5 
                            }
                        }
                    ))
                    
                    fig.update_layout(
                        height=260, 
                        margin=dict(l=25, r=25, t=50, b=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Plus Jakarta Sans", color="#0C1A13")
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
            st.markdown('<div class="section-header">Top Attrition Drivers for This Profile</div>', unsafe_allow_html=True)
            
            factors_df = get_top_contributions(processed_input, top_n=5)
            
            if not factors_df.empty:
                with st.container(border=True):
                    # Styled Plotly Bar Chart for High Contrast Dark Text on Light Card
                    fig = px.bar(
                        factors_df,
                        y="factor",
                        x="impact",
                        color="direction",
                        color_discrete_map={"increases risk": "#DC2626", "decreases risk": "#0F766E"},
                        title="Primary Model Feature Impacts",
                        orientation='h',
                        text="impact"
                    )
                    
                    fig.update_traces(
                        texttemplate='%{text:.2f}', 
                        textposition='outside',
                        textfont=dict(color="#0C1A13", size=13, family="Plus Jakarta Sans"),
                        marker=dict(line=dict(width=0))
                    )
                    
                    fig.update_layout(
                        height=360,
                        xaxis_title="Relative Impact Magnitude",
                        yaxis_title="",
                        legend_title="Impact Direction",
                        margin=dict(l=20, r=30, t=50, b=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Plus Jakarta Sans", color="#0C1A13"),
                        title=dict(font=dict(color="#0C1A13", size=16, family="Playfair Display")),
                        legend=dict(font=dict(color="#0C1A13")),
                        yaxis=dict(
                            autorange="reversed", 
                            gridcolor="rgba(0,0,0,0)",
                            tickfont=dict(color="#0C1A13", size=12, family="Plus Jakarta Sans")
                        ),
                        xaxis=dict(
                            gridcolor="#C5B89F",
                            title_font=dict(color="#0C1A13"),
                            tickfont=dict(color="#0C1A13")
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("View Raw Transformed Inputs"):
                st.json(user_inputs)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="section-header" style="margin-top:0;">Predictive Model Spec</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("""
        <span style="color:#0C1A13; font-weight:700;">Architecture:</span> <span style="color:#2E4E3C;">Logistic Regression with L2 Regularization & Feature Engineering Pipeline.</span><br><br>
        <span style="color:#0C1A13; font-weight:700;">Key Input Dimensions:</span>
        <ul style="color:#2E4E3C; padding-left:20px; margin-top:4px;">
            <li>Demographics: Age, Gender, Marital Status</li>
            <li>Job Context: Role, Department, Business Travel</li>
            <li>Compensation: Income, Salary Hike %, Options</li>
            <li>Satisfaction: Job, Environment, Work-Life Balance</li>
            <li>Tenure: Total Experience & Promotion History</li>
        </ul>
        <span style="color:#0C1A13; font-weight:700;">Model Benchmark:</span>
        <ul style="color:#2E4E3C; padding-left:20px; margin-top:4px;">
            <li>Accuracy: ~86% on test validation set</li>
            <li>Threshold Tuning: 53.5% decision cut-off for optimal precision-recall balance.</li>
        </ul>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Guidance</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("""
        <ol style="color:#2E4E3C; padding-left:20px; margin:0;">
            <li>Complete all employee metrics.</li>
            <li>Evaluate Risk Index & Primary Drivers.</li>
            <li>Combine quantitative outputs with qualitative manager feedback.</li>
        </ol>
        """, unsafe_allow_html=True)
    
    st.caption("Attrition Risk Evaluator.")