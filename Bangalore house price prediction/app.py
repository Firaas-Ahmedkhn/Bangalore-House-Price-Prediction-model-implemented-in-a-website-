import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import plotly.express as px

# Load the model
pickle_in = open("Model.pkl", "rb")
lr = pickle.load(pickle_in)

df = pd.read_csv("Cleaned_data.csv")

nav = st.sidebar.radio("Navigation", ["Home", "Predict", "Contact us"])

if nav == "Home":
    st.title("HOME.AI")
    st.markdown("__________")
    st.subheader("Bangalore House Price Prediction")
    st.image("image.jpeg", width=500)
    if st.checkbox("Show Table"):
        st.table(df)

    graph = st.selectbox("What kind of graph?", ["Non-Interactive", "Interactive"])

    if graph == "Non-Interactive":
        fig, ax = plt.subplots(figsize=(10, 5))
        plt.scatter(df["bhk"], df["price"])
        plt.ylim(0)
        plt.xlabel("Size(bhk)")
        plt.ylabel("Price")
        plt.tight_layout()
        st.pyplot(fig)    

    if graph == "Interactive":
        val = st.slider("Filter data using size", 0, 30)
        filtered_df = df.loc[df["bhk"] >= val]
        fig = px.scatter(filtered_df, x="bhk", y="price")
        st.plotly_chart(fig)

if nav == "Predict":
    def predict_price(location, bhk, bath, total_sqft):
        if not location:
            return "Please select a location."

        location = location[0]

        input_data = pd.DataFrame({'location': [location], 'bhk': [bhk], 'bath': [bath], 'total_sqft': [total_sqft]})

        # Use the model to make predictions
        prediction = lr.predict(input_data)
        return prediction

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

        # Adding the user input to our cleaned data to make our model more accurate
        to_add = {"location":location, "bhk":bhk, "bath":bath, "total_sqft": total_sqft, "price": result}
        to_add = pd.DataFrame(to_add)
        to_add.to_csv("Cleaned_data.csv", mode='a', header=False, index=False)    
    



if nav == "Contact us":
    st.title("Contact us")
    st.markdown("_________")
    st.subheader("Created by Firaas Ahmed Khan")
    st.text("B.Tech Artificial Intelligence student from Zakir Husain College of Engineering & Technology, AMU, Aligarh")
    st.markdown("[LinkedIn](www.linkedin.com/in/firaas-akhan)")
    st.markdown("[GitHub](https://github.com/Firaas-Ahmedkhn)")
    st.text("Gmail- firaaskhan@gmail.com")
