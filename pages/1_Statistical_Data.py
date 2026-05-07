import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Analysis", page_icon="📊")

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

df = load_data()

st.title("📊 Data Analysis")
st.write("Browse through the raw dataset and basic statistical analysis.")

# 1. Dataset Preview
st.subheader("Dataset Preview")
st.write("Current Columns:", list(df.columns))

# Extract numeric columns dynamically for safe rounding
numeric_cols = df.select_dtypes(include='number').columns

# Apply a clean light theme and round formatting to the raw dataset
styled_preview = df.style.format("{:.2f}", subset=numeric_cols) \
                         .set_properties(**{'background-color': '#f8f9fa', 'color': '#212529'}) \
                         .highlight_max(subset=numeric_cols, color='#d4edda', axis=0)
st.dataframe(styled_preview, use_container_width=True)

# 2. Overall Averages
st.subheader("Overall Averages")
st.write("The mean score for each parameter across the entire dataset:")
overall_avg = df.mean(numeric_only=True).to_frame(name="Overall Average Score")

# Apply a beautiful cool blue color gradient theme
styled_overall = overall_avg.style.format("{:.2f}") \
                                  .background_gradient(cmap='Blues', axis=0) \
                                  .set_properties(**{'border': '1px solid white'})
st.dataframe(styled_overall, use_container_width=True)

# 3. Meal-wise Averages
st.subheader("Meal-wise Averages")
st.write("The average scores grouped by the meal type:")
meal_avg = df.groupby("Meal").mean(numeric_only=True)

# Apply a warm sunset color gradient to highlight varying meal experiences
styled_meal = meal_avg.style.format("{:.2f}") \
                            .background_gradient(cmap='Oranges', axis=0) \
                            .set_properties(**{'border': '1px solid white'})
st.dataframe(styled_meal, use_container_width=True)
