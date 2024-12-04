import pandas as pd
import streamlit as st
import plotly.express as px

data=pd.read_csv('vehicles_us.csv')

columns_to_replace = ['paint_color', 'is_4wd']
for column in columns_to_replace:
    data[column]= data[column].fillna('unknown')
    
data['model_year'] = data['model_year'].fillna(data.groupby(['model'])
['model_year'].transform('median'))
data['model_year'] = data['model_year'].apply( lambda x: int(x))

data['cylinders'] = pd.to_numeric(data['cylinders'])
data['cylinders'] = data['cylinders'].fillna(data.groupby(['model'])
['cylinders'].transform('mean'))

data['odometer'] = data['odometer'].fillna(data.groupby(['model_year'])['odometer'].transform('median'))
data['odometer'] = data['odometer'].round()

replacement_dict = {
    'chevrolet camaro lt coupe 2d': 'chevrolet camaro',
    'ford f-250 sd': 'ford f-250',
    'ford f-250 super duty': 'ford f-250',
    'ford f250': 'ford f-250',
    'ford f250 super duty': 'ford f-250',
    'ford f-350 sd': 'ford f-350',
    'ford f350': 'ford f-350',
    'ford f350 super duty': 'ford f-350',
    'honda civic lx': 'honda civic',
    'jeep grand cherokee laredo': 'jeep grand cherokee',
    'nissan frontier crew cab sv': 'nissan frontier',
    'toyota camry le': 'toyota camry',
}

data['model'] = data['model'].replace(replacement_dict)

# Identify IQR for model_year and price
Q1_model_year = data['model_year'].quantile(0.25)
Q3_model_year = data['model_year'].quantile(0.75)
IQR_model_year = Q3_model_year - Q1_model_year

Q1_price = data['price'].quantile(0.25)
Q3_price = data['price'].quantile(0.75)
IQR_price = Q3_price - Q1_price

# Define outlier boundaries
model_year_lower = Q1_model_year - 1.5 * IQR_model_year
model_year_upper = Q3_model_year + 1.5 * IQR_model_year

price_lower = Q1_price - 1.5 * IQR_price
price_upper = Q3_price + 1.5 * IQR_price

data = data[
    (data['model_year'] >= model_year_lower) & (data['model_year'] <= model_year_upper) &
    (data['price'] >= price_lower) & (data['price'] <= price_upper)]

st.title('Choose your vehicle!')
st.header('Use this app to select a vehicle on the market')

price_range = st.slider(
    "What is your price range?",
    min_value=1, 
    max_value=37500,  
    value=(1, 37500)  
)

actual_range=list(range(price_range[0], price_range[1]+1))
filtered_data=data[data.price.isin(actual_range)] 

low_odometer = st.checkbox('Only low odometer')

if low_odometer:
    filtered_data = data[data['price'].isin(actual_range) & (data['odometer'] <= 15000)]
else:
    filtered_data = data[data['price'].isin(actual_range)]
    
st.write = ('Here are your options with a split by price and odometer')

fig = px.scatter(filtered_data, x='odometer', y='price', title="Vehicle Price vs. Odometer Reading")
st.plotly_chart(fig)

st.write=('Distribution of price of filtered vehicles')

fig2=px.histogram(filtered_data, x='price', title="Price Distribution")
st.plotly_chart(fig2)

