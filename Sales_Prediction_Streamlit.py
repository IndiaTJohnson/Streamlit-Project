#Imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
pd.set_option('display.max_columns',100)
import plotly.express as px
import plotly.io as pio



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


# Add a selectbox for all possible features
column = st.selectbox(label="Select a column", options=df.columns)

# Use plotly for explore functions
def plotly_explore_numeric(df, x):
    fig = px.histogram(df,x=x,marginal='box',title=f'Distribution of {x}', 
                      width=1000, height=500)
    return fig
def plotly_explore_categorical(df, x):
    fig = px.histogram(df,x=x,color=x,title=f'Distribution of {x}', 
                          width=1000, height=500)
    fig.update_layout(showlegend=False)
    return fig
# Conditional statement to determine which function to use
if df[column].dtype == 'object':
    fig = plotly_explore_categorical(df, column)
else:
    fig = plotly_explore_numeric(df, column)
    
st.markdown("#### Displaying appropriate Plotly plot based on selected column")
# Display appropriate eda plots
st.plotly_chart(fig)


columns_to_use = df.columns.to_list()


st.markdown("#### Explore Features vs. Item_MRP with Plotly")
# Add a selectbox for all possible features (exclude SalePrice)
# Copy list of columns
features_to_use = columns_to_use[:]
# Define target
target = 'Item_MRP'
# Remove target from list of features
features_to_use.remove(target)

# Add a selectbox for all possible columns
feature = st.selectbox(label="Select a feature to compare with Item_MRP", options=features_to_use)

# functionizing numeric vs target
def plotly_numeric_vs_target(df, x, y=target, trendline='ols',add_hoverdata=True):
    if add_hoverdata == True:
        hover_data = list(df.columns)
    else: 
        hover_data = None
        
    pfig = px.scatter(df, x=x, y=y,width=800, height=600,
                     hover_data=hover_data,
                      trendline=trendline,
                      trendline_color_override='red',
                     title=f"{x} vs. {y}")
    
    pfig.update_traces(marker=dict(size=3),
                      line=dict(dash='dash'))
    return pfig



def plotly_categorical_vs_target(df, x, y=target, histfunc='avg', width=800,height=500):
    fig = px.histogram(df, x=x,y=y, color=x, width=width, height=height,
                       histfunc=histfunc, title=f'Compare {histfunc.title()} {y} by {x}')
    fig.update_layout(showlegend=False)
    return fig

# Conditional statement to determine which function to use
if df[feature].dtype == 'object':
    fig_vs  = plotly_categorical_vs_target(df, x = feature)
else:
    fig_vs  = plotly_numeric_vs_target(df, x = feature)

st.plotly_chart(fig_vs)