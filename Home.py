#streamlit run "Home.py"
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Mess Feedback Dashboard", 
    page_icon="🍔",
    layout="centered"
)

# Use cache to load data efficiently
@st.cache_data
def load_data():
    df = pd.read_csv("Updated PVGCOET Mess Feedback.csv")
    
    # Rename columns
    df.rename(columns={
        "MEAL TYPE(Choose the meal you just had)": "Meal",
        "Food Temperature": "Temperature",
        "Your Experience": "Experience",
        "Taste  ": "Taste"
    }, inplace=True)
    
    # Drop Timestamp column
    if 'Timestamp' in df.columns:
        df.drop(columns=['Timestamp'], inplace=True)
        
    return df

# Load the data
df = load_data()

# Page Content
st.title("🍔 Mess Feedback Dashboard")
st.write("Welcome to the Mess Feedback Dashboard! This application provides structured insights into student feedback. Use the sidebar to navigate between Data Analysis and Visualizations.")

st.subheader("Key Metrics")

# Calculate metrics
total_responses = len(df)
# Overall average rating across all numeric parameter columns
numeric_cols = df.select_dtypes(include='number').columns
overall_avg = df[numeric_cols].mean().mean() 

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Responses", total_responses)
with col2:
    st.metric("Overall Average Rating", f"{overall_avg:.2f} / 5.0")

st.info("👈 Please select a page from the sidebar to view the details!")
