import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
data_path = 'C:\\flood_pred_app\\flood_pred_dummy_sheet.xlsx'
data = pd.read_excel(data_path)

# Set page configuration
st.set_page_config(page_title="Flood Prediction Analysis", layout="wide")
st.title("Flood Prediction Analysis Dashboard")
st.write("Interactive analysis of water levels, danger levels, and seasonal flood trends across rivers and stations.")

# Sidebar filters
st.sidebar.header("Filter Data")
selected_river = st.sidebar.selectbox("Select River", options=data["River"].unique())
stations = data[data["River"] == selected_river]["Station"].unique()
selected_station = st.sidebar.selectbox("Select Station", options=stations)

# Filter data based on selections
filtered_data = data[(data["River"] == selected_river) & (data["Station"] == selected_station)]

# Time Series Analysis of Water Levels
st.subheader(f"Water Level Trends Over Time: {selected_river} River at {selected_station}")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_data, x='Date', y='Todays Level', ax=ax, label='Todays Level')
sns.lineplot(data=filtered_data, x='Date', y='Danger Level', ax=ax, label='Danger Level', color='red', linestyle='--')
ax.set_title("Daily Water Levels vs. Danger Levels")
plt.xticks(rotation=45)
st.pyplot(fig)

# Seasonal Pattern Analysis
st.subheader("Monthly Average Water Levels")
filtered_data['Month'] = filtered_data['Date'].dt.month
monthly_data = filtered_data.groupby('Month')['Todays Level'].mean().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=monthly_data, x='Month', y='Todays Level', palette='viridis')
ax.set_title(f"Monthly Water Levels for {selected_river} River at {selected_station}")
st.pyplot(fig)

# Difference from Danger Level
st.subheader(f"Difference from Danger Level Over Time: {selected_river} River at {selected_station}")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_data, x='Date', y='Difference from Danger Level', ax=ax, color="purple")
ax.axhline(0, color="gray", linestyle="--", linewidth=1)
ax.set_title("Difference from Danger Level")
plt.xticks(rotation=45)
st.pyplot(fig)

# River and Station Distribution Analysis
st.subheader(f"Water Level Distribution for {selected_river} River at {selected_station}")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_data["Todays Level"], kde=True, ax=ax, color='teal')
ax.set_title("Distribution of Today's Water Level")
st.pyplot(fig)

# Annual Maximum Flood Levels
st.subheader("Historical Maximum Flood Levels")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_data, x='Year', y='Maximum Flood Level', ax=ax, marker='o', color="darkblue")
ax.set_title(f"Annual Maximum Flood Levels for {selected_river} River at {selected_station}")
plt.xticks(rotation=45)
st.pyplot(fig)

# Correlation Analysis
st.subheader("Correlation Matrix of Water Level Variables")
numeric_cols = ["Maximum Flood Level", "Danger Level", "Todays Level", "Difference from Danger Level"]
correlation_data = filtered_data[numeric_cols].dropna().corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title("Correlation Matrix")
st.pyplot(fig)

# Additional Insights and Notes
st.sidebar.subheader("Additional Insights")
st.sidebar.write("This dashboard provides insights into flood trends and potential danger periods.")
st.sidebar.write("Data visualizations such as time series analysis, monthly averages, and correlation analysis can be used to better understand flood patterns and inform predictive models.")

st.sidebar.write("---")
st.sidebar.write("Developed by IIIT Lucknow")
