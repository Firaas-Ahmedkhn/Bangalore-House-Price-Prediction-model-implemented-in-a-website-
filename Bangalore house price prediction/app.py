import streamlit as st
import pandas as pd
import pickle

# Load the model
pickle_in = open("Model.pkl", "rb")
lr = pickle.load(pickle_in)

df = pd.read_csv("Cleaned_data.csv")

def predict_price(location, bhk, bath, total_sqft):
    input_data = pd.DataFrame({'location': [location], 'bhk': [bhk], 'bath': [bath], 'total_sqft': [total_sqft]})
    
    # Use the model to make predictions
    prediction = lr.predict(input_data)
    return prediction

def main():
    st.title("HOME.AI")
    st.markdown("_______")
    html_temp = """
    <style>
        .header {
            font-size: 32px;
            color: #ffffff;
            text-align: left;
            margin-bottom: 10px;
        }
        .description {
            font-size: 18px;
            color: #ffffff;
            text-align: left;
            margin-bottom: 20px;
        }
        .app {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
            position: relative;
        }
    </style>
    <div class="header">Bangalore House Price Prediction</div>
    <div class="description">Predict the price of your dream home in Bangalore!</div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    location = st.multiselect("Location", df['location'], placeholder="Select location")
    bhk = st.text_input("BHK", placeholder="Type here", key='bhk')
    bath = st.text_input("Bath", placeholder="Type here", key='bath')
    total_sqft = st.text_input("Total Sqft", placeholder="Type here", key='total_sqft')

    if st.button("Predict"):
        try:
            result = predict_price(location, bhk, bath, total_sqft)
            st.success(f'Predicted price is Rs.{result[0]:,.2f}')
        except Exception as e:
            st.error("Error making prediction. Please check your inputs.")

    if st.button("About"):
        st.text("Created by Firaas Ahmed Khan")

if __name__ == '__main__':
    main()
