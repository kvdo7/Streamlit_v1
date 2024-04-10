import streamlit as st
import pandas as pd
import numpy as np
import pickle
import base64

# Correct paths for the files
loan_image_path = 'C:/Users/solar7/Downloads/Streamlit1/loan_image.jpg'
model_path = 'C:/Users/solar7/Downloads/Streamlit1/RF.sav'
rain_gif_path = 'C:/Users/solar7/Downloads/Streamlit1/6m-rain.gif'
no_gif_path = 'C:/Users/solar7/Downloads/Streamlit1/green-cola-no.gif'
data_path = 'C:/Users/solar7/Downloads/Streamlit1/test.csv'  # Corrected to point to the CSV file

# Replace @st.experimental_memo with @st.cache_data
@st.cache_data
def get_fvalue(val):    
    feature_dict = {"No":1, "Yes":2}    
    return feature_dict.get(val, 0)

def get_value(val, my_dict):    
    return my_dict.get(val, 0)

app_mode = st.sidebar.selectbox('Select Page', ['Home', 'Prediction'])

if app_mode == 'Home':
    st.title('LOAN PREDICTION APP')
    st.image(loan_image_path)  # Updated path
    st.markdown('Dataset :')    
    data = pd.read_csv(data_path)  # Updated to use pd.read_csv for a CSV file
    st.write(data.head())
    st.markdown('Applicant Income VS Loan Amount')
    st.bar_chart(data[['ApplicantIncome', 'LoanAmount']].head(20))

elif app_mode == 'Prediction':
    st.subheader('Fill in the information to get your loan status prediction')
    
    # Dictionary setups for user input conversion
    gender_dict = {"Male": 1, "Female": 2}
    feature_dict = {"No": 1, "Yes": 2}
    edu = {'Graduate': 1, 'Not Graduate': 2}
    prop = {'Rural': 1, 'Urban': 2, 'Semiurban': 3}
    
    # Collecting user inputs
    ApplicantIncome = st.sidebar.slider('ApplicantIncome', 0, 10000, 5000)
    CoapplicantIncome = st.sidebar.slider('CoapplicantIncome', 0, 10000, 0)
    LoanAmount = st.sidebar.slider('LoanAmount in K$', 9.0, 700.0, 200.0)
    Loan_Amount_Term = st.sidebar.selectbox('Loan_Amount_Term', (12.0, 36.0, 60.0, 84.0, 120.0, 180.0, 240.0, 300.0, 360.0))
    Credit_History = st.sidebar.radio('Credit_History', (0.0, 1.0))
    Gender = st.sidebar.radio('Gender', tuple(gender_dict.keys()))
    Married = st.sidebar.radio('Married', tuple(feature_dict.keys()))
    Self_Employed = st.sidebar.radio('Self Employed', tuple(feature_dict.keys()))
    Dependents = st.sidebar.radio('Dependents', options=['0', '1', '2', '3+'])
    Education = st.sidebar.radio('Education', tuple(edu.keys()))
    Property_Area = st.sidebar.radio('Property_Area', tuple(prop.keys()))
    
    # Encoding user inputs
    class_0, class_1, class_2, class_3 = 0, 0, 0, 0    
    if Dependents == '0': class_0 = 1    
    elif Dependents == '1': class_1 = 1   
    elif Dependents == '2': class_2 = 1    
    else: class_3 = 1

    Rural, Urban, Semiurban = 0, 0, 0    
    if Property_Area == 'Urban': Urban = 1    
    elif Property_Area == 'Semiurban': Semiurban = 1    
    else: Rural = 1
    
    # Preparing the input vector
    feature_list = [ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, get_value(Gender, gender_dict), get_fvalue(Married), class_0, class_1, class_2, class_3, get_value(Education, edu), get_fvalue(Self_Employed), Rural, Urban, Semiurban]
    single_sample = np.array(feature_list).reshape(1, -1)
    
    # Prediction and displaying results
    if st.button("Predict"):
        with open(model_path, 'rb') as f:
            loaded_model = pickle.load(f)
        
        prediction = loaded_model.predict(single_sample)
        
        # Displaying GIF based on prediction
        if prediction[0] == 0:
            st.error('According to our calculations, you will not get the loan from the bank.')
            file_path = no_gif_path
        else:
            st.success('Congratulations! According to our calculations, you will get the loan from the bank.')
            file_path = rain_gif_path
        
        file_ = open(file_path, "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="result gif">', unsafe_allow_html=True)
