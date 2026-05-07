import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Visualizations", page_icon="📈", layout="wide")

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

st.title("📈 Visualizations")
st.write("Visual representations of the mess feedback data.")

# 1. Bar Chart: Average Taste by Meal
st.subheader("1. Average Taste by Meal")
meal_taste_avg = df.groupby("Meal")["Taste"].mean().reset_index()

fig_taste, ax_taste = plt.subplots(figsize=(8, 4))
colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0', '#FFB3E6']
colors = colors * (len(meal_taste_avg) // len(colors) + 1)

bars = ax_taste.bar(
    meal_taste_avg["Meal"], 
    meal_taste_avg["Taste"], 
    color=colors[:len(meal_taste_avg)], 
    edgecolor='#333333', 
    linewidth=1.2
)

ax_taste.set_title("Average Taste Rating per Meal", fontsize=16, fontweight='bold', color='#2C3E50', pad=15)
ax_taste.set_xlabel("Meal Type", fontsize=12, fontweight='bold', color='#34495E')
ax_taste.set_ylabel("Taste Rating", fontsize=12, fontweight='bold', color='#34495E')
ax_taste.tick_params(axis='x', labelsize=11, labelrotation=0)
ax_taste.grid(axis='y', linestyle='--', alpha=0.6)
ax_taste.spines['top'].set_visible(False)
ax_taste.spines['right'].set_visible(False)

for bar in bars:
    yval = bar.get_height()
    ax_taste.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f"{yval:.2f}", ha='center', va='bottom', fontweight='bold')
    
st.pyplot(fig_taste)


# 2. Pie Chart: Meal distribution
st.divider()
st.subheader("2. Distribution of Meal Types")
meal_counts = df["Meal"].value_counts()

fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
ax_pie.pie(
    meal_counts, 
    labels=meal_counts.index, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=['#FF9999', '#66B3FF', '#99FF99', '#FFCC99'], 
    textprops={'fontsize': 12, 'fontweight': 'bold', 'color': '#2C3E50'},
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
)
ax_pie.set_title("Proportion of Responses by Meal", fontsize=16, fontweight='bold', color='#2C3E50', pad=15)
st.pyplot(fig_pie)


# 3. Bar Chart: All parameters Across Meals
st.divider()
st.subheader("3. All Parameters Across Meals (Stacked Comparison)")
grouped = df.groupby("Meal").mean(numeric_only=True)
all_cols = ["Taste", "Temperature", "Quantity", "Hygiene", "Experience"]
all_cols = [c for c in all_cols if c in grouped.columns]

fig_stack, ax_stack = plt.subplots(figsize=(10, 6))
grouped[all_cols].plot(
    kind='bar', 
    stacked=True, 
    ax=ax_stack, 
    color=['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0'],
    edgecolor='#333333',
    linewidth=1.2
)

ax_stack.set_title("Overall Parameter Analysis by Meal Type", fontsize=16, fontweight='bold', color='#2C3E50', pad=15)
ax_stack.set_xlabel("Meal Type", fontsize=12, fontweight='bold', color='#34495E')
ax_stack.set_ylabel("Cumulative Score", fontsize=12, fontweight='bold', color='#34495E')
ax_stack.tick_params(axis='x', rotation=0, labelsize=11)
ax_stack.grid(axis='y', linestyle='--', alpha=0.6)
ax_stack.spines['top'].set_visible(False)
ax_stack.spines['right'].set_visible(False)
ax_stack.legend(title='Parameters', bbox_to_anchor=(1.05, 1), loc='upper left')

st.pyplot(fig_stack)


# 4. Bar Chart: Overall Average of Each Parameter
st.divider()
st.subheader("4. Overall Average of Each Parameter")

# Calculate overall average for the specific numeric columns requested
overall_avg = df.mean(numeric_only=True)
important_cols = ["Taste", "Temperature", "Quantity", "Hygiene", "Experience"]
cols_to_plot = [c for c in important_cols if c in overall_avg.index]

# Display as a simple bar chart
st.bar_chart(overall_avg[cols_to_plot])

