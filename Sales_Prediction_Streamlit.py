#Imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
pd.set_option('display.max_columns',100)




st.title('Sales Price Analysis')
st.header("Product Sales Data")

# Function for loading data
# Adding data caching
@st.cache_data
def load_data():
    fpath =  "Data/new_sales_predictions_2023.csv"
    df = pd.read_csv(fpath)
    return df


# load the data 
df = load_data()
# Display an interactive dataframe
st.header("Displaying a DataFrame")
st.dataframe(df, width=800)


st.subheader("Descriptive Statistics")

if st.button("Show Descriptive Statistics"):
    st.dataframe(df.describe().round(2))

st.subheader("Summary Info")
# Capture .info()
# Create a string buffer to capture the content
buffer = StringIO()
# Write the info into the buffer
df.info(buf=buffer)
# Retrieve the content from the buffer
summary_info = buffer.getvalue()

if st.button("Show Summary Info"):
    st.text(summary_info)


st.subheader("Null Values")
nulls =df.isna().sum()
if st.button("Show Null Values"):
    st.dataframe(nulls)