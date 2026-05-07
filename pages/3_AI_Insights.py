import streamlit as st
import pandas as pd
import os
import re
import requests
import json
from dotenv import load_dotenv

# 1. Load the API key securely using dotenv and os.getenv.
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="AI Insights", page_icon="🤖", layout="wide")

# 8. Clean and modern Streamlit UI
st.title("🤖 AI Insights")
st.markdown("Automated insights and recommendations generated from the latest mess feedback dataset.")

# Custom CSS for spacing and minor styling
st.markdown(
    """
    <style>
    .error-box {
        background-color: #ffebee;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #f44336;
        color: #b71c1c;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #2196f3;
        color: #0d47a1;
        margin-bottom: 20px;
    }
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_data():
    try:
        # 4. Read the existing mess feedback CSV dataset
        df = pd.read_csv("Updated PVGCOET Mess Feedback.csv")
        
        # Rename columns to be more concise
        df.rename(columns={
            "MEAL TYPE(Choose the meal you just had)": "Meal",
            "Food Temperature": "Temperature",
            "Your Experience": "Experience",
            "Taste  ": "Taste"
        }, inplace=True)
        
        if 'Timestamp' in df.columns:
            df.drop(columns=['Timestamp'], inplace=True)
            
        return df
    except Exception as e:
        return None

df = load_data()

# 9. Add basic error handling
if not API_KEY:
    st.markdown('<div class="error-box"><strong>Error:</strong> OPENROUTER_API_KEY is missing in the .env file. Please configure it to use AI Insights.</div>', unsafe_allow_html=True)
    st.stop()

if df is None or df.empty:
    st.markdown('<div class="error-box"><strong>Error:</strong> Dataset could not be loaded or is empty. Please check the data source.</div>', unsafe_allow_html=True)
    st.stop()

st.markdown('<div class="info-box">Dataset loaded successfully. Click the button below to analyze the feedback.</div>', unsafe_allow_html=True)
st.write("") # Spacer

if st.button("Generate AI Insights 🚀", type="primary"):
    # 12. Make the AI prompt concise and optimized
    # Calculate some summary stats to pass along with data
    summary_stats = df.describe().to_csv()
    raw_data_csv = df.to_csv(index=False)
    
    prompt = f"""
    You are an expert data analyst. I am providing you with student feedback data for a mess/cafeteria.
    The scores are out of 5 for Taste, Temperature, Quantity, Hygiene, and Experience.
    
    Here is the summary statistics of the dataset:
    {summary_stats}
    
    Here is the raw data (excluding timestamps):
    {raw_data_csv}
    
    Please analyze this data and provide insights structured EXACTLY with these markdown headings:
    ### Overall Summary
    ### Positive Insights
    ### Negative Insights
    ### Suggestions
    
    Keep the insights concise, actionable, and directly focused on the provided data.
    """
    
    # 7. Add a loading spinner while generating the AI response
    with st.spinner("Analyzing dataset and generating insights... Please wait ⏳"):
        try:
            # 3. Use model: google/gemma-3-31b-it:free directly via requests to OpenRouter
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            # Gemma does not support 'system' role — merge instruction into user message
            full_prompt = "You are a helpful AI assistant analyzing mess feedback data.\n\n" + prompt

            payload = {
                "model": "google/gemma-4-31b-it:free",
                "messages": [
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                st.markdown(f'<div class="error-box"><strong>API Error {response.status_code}:</strong> {response.text}</div>', unsafe_allow_html=True)
                st.stop()
            
            ai_content = response.json()["choices"][0]["message"]["content"]
            
            st.success("✨ Analysis complete!")
            st.markdown("---")
            
            # 5 & 6. Structure the output with clear headings and styled containers
            # Parse the markdown to put sections into Streamlit native styled containers
            sections = re.split(r'(?i)###\s*', ai_content)
            
            # If the model didn't use ### exactly as requested, fallback to normal display
            if len(sections) < 2:
                st.markdown(ai_content)
            else:
                for section in sections:
                    if not section.strip():
                        continue
                    parts = section.split('\n', 1)
                    heading = parts[0].strip()
                    content = parts[1].strip() if len(parts) > 1 else ""
                    
                    # 8. Styled containers/cards mapping based on heading type
                    if "Overall Summary" in heading:
                        st.subheader("📊 " + heading)
                        st.info(content)
                    elif "Positive Insights" in heading:
                        st.subheader("✅ " + heading)
                        st.success(content)
                    elif "Negative Insights" in heading:
                        st.subheader("⚠️ " + heading)
                        st.warning(content)
                    elif "Suggestions" in heading:
                        st.subheader("💡 " + heading)
                        st.info(content)
                    else:
                        st.subheader(heading)
                        st.write(content)
                        
        except Exception as e:
            st.markdown(f'<div class="error-box"><strong>API Error:</strong> Failed to generate insights. Details: {str(e)}</div>', unsafe_allow_html=True)
