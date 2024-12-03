import streamlit as st
import pandas as pd
import plotly.express as px

data=pd.read_csv('C:/Users/galia/Documents/vehicles sprint 6 project/vehicles/vehicles_us.csv')

st.title('Choose your vehicle!')
st.header('Use this app to select a vehicle on the market')

price_range = st.slider(
    "What is your price range?",
    min_value=1, 
    max_value=37500,  
    value=(1, 37500)  
)

actual_range=list(range(price_range[0], price_range[1]+1))

low_odometer = st.checkbox('Only low odometer')

if low_odometer:
    filtered_data = data[data['price'].isin(actual_range) & (data['odometer'] <= 15000)]
else:
    filtered_data = data[data['price'].isin(actual_range)]
    
st.write('Here are your options with a split by price and odometer')

fig = px.scatter(filtered_data, x='odometer', y='price', title="Vehicle Price vs. Odometer Reading")
st.plotly_chart(fig)

st.write=('Distribution of price of filtered vehicles')

fig2=px.histogram(filtered_data, x='price', title="Price Distribution")
st.plotly_chart(fig2)

