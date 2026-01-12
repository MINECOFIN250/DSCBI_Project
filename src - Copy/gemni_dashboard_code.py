import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. Data Acquisition & Preparation (Simulated for demonstration) ---
# In a real application, you would load this from APIs, CSVs, or a database.
def load_data():
    years = np.arange(2010, 2026) # Up to 2023 historical, 2024-2025 projection
    data = []

    # Simulate GDP Growth (Annual %)
    gdp_growth = np.random.uniform(3, 8, len(years))
    # Simulate a slight dip and recovery, then projected growth
    gdp_growth[np.isin(years, [2020, 2021])] = np.random.uniform(0.5, 4, 2)
    gdp_growth[np.isin(years, [2024, 2025])] = np.random.uniform(7, 9, 2) # Projection
    gdp_growth = np.round(gdp_growth, 2)

    # Simulate Inflation Rate (CPI %)
    inflation_rate = np.random.uniform(2, 12, len(years))
    inflation_rate[np.isin(years, [2022, 2023])] = np.random.uniform(8, 15, 2) # Higher recent inflation
    inflation_rate[np.isin(years, [2024, 2025])] = np.random.uniform(5, 7, 2) # Projected decrease
    inflation_rate = np.round(inflation_rate, 2)

    # Simulate Unemployment Rate (%)
    unemployment_rate = np.random.uniform(2, 8, len(years))
    unemployment_rate[np.isin(years, [2020, 2021])] = np.random.uniform(6, 12, 2) # Higher during crisis
    unemployment_rate[np.isin(years, [2024, 2025])] = np.random.uniform(3, 5, 2) # Projected decrease
    unemployment_rate = np.round(unemployment_rate, 2)

    for i, year in enumerate(years):
        data.append({
            'Year': year,
            'Sector': 'Overall Economy', # Simplified for this example
            'Indicator': 'GDP Growth (Annual %)',
            'Value': gdp_growth[i],
            'Type': 'Projection' if year > 2023 else 'Historical'
        })
        data.append({
            'Year': year,
            'Sector': 'Overall Economy',
            'Indicator': 'Inflation Rate (CPI %)',
            'Value': inflation_rate[i],
            'Type': 'Projection' if year > 2023 else 'Historical'
        })
        data.append({
            'Year': year,
            'Sector': 'Overall Economy',
            'Indicator': 'Unemployment Rate (%)',
            'Value': unemployment_rate[i],
            'Type': 'Projection' if year > 2023 else 'Historical'
        })
    
    df = pd.DataFrame(data)
    return df

df = load_data()
all_sectors = sorted(df['Sector'].unique())
all_indicators = sorted(df['Indicator'].unique())
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())


# --- 2. Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="Rwanda's Economy Macroeconomic Dashboard")

st.title("RWANDA'S ECONOMY MACROECONOMIC DASHBOARD")
st.subheader("Macro-Economic Indicators - Historical & Projections")

# --- Selection Panel (Sidebar) ---
st.sidebar.header("SELECTION PANEL")

# Sector selection
selected_sector = st.sidebar.selectbox("Sector", all_sectors, index=0)

# Indicator selection (two dropdowns for two charts)
st.sidebar.subheader("Indicators for Charts")
indicator_1 = st.sidebar.selectbox("Indicator 1", all_indicators, index=0)
indicator_2 = st.sidebar.selectbox("Indicator 2", all_indicators, index=1)

# Year range selection
selected_years = st.sidebar.slider(
    "Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Historical Trend and Projection toggles
st.sidebar.subheader("Display Options")
show_historical = st.sidebar.checkbox("Historical Trend", value=True)
show_projection = st.sidebar.checkbox("Projection", value=True)

# --- Filter Data Based on Selections ---
filtered_df = df[
    (df['Sector'] == selected_sector) &
    (df['Year'] >= selected_years[0]) &
    (df['Year'] <= selected_years[1])
]

# Apply historical/projection filter
if not show_historical:
    filtered_df = filtered_df[filtered_df['Type'] == 'Projection']
if not show_projection:
    filtered_df = filtered_df[filtered_df['Type'] == 'Historical']
if not show_historical and not show_projection: # If both are unchecked, show nothing
    filtered_df = pd.DataFrame() # Empty dataframe

# --- Body with Two Charts ---
st.write("---")
st.header("Historical Trend and Projection")

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"{indicator_1} Trend")
    if not filtered_df.empty and indicator_1 in filtered_df['Indicator'].unique():
        chart_df_1 = filtered_df[filtered_df['Indicator'] == indicator_1]
        fig1 = px.line(chart_df_1, x='Year', y='Value', 
                       title=f'{indicator_1} Over Time',
                       markers=True,
                       color='Type', # Differentiate historical vs projection
                       color_discrete_map={'Historical': 'blue', 'Projection': 'green'})
        fig1.update_traces(marker=dict(size=8))
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info(f"No data available for {indicator_1} with current selections.")


with col2:
    st.subheader(f"{indicator_2} Trend")
    if not filtered_df.empty and indicator_2 in filtered_df['Indicator'].unique():
        chart_df_2 = filtered_df[filtered_df['Indicator'] == indicator_2]
        fig2 = px.bar(chart_df_2, x='Year', y='Value', 
                      title=f'{indicator_2} Over Time',
                      color='Type', # Differentiate historical vs projection
                      color_discrete_map={'Historical': 'orange', 'Projection': 'purple'})
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info(f"No data available for {indicator_2} with current selections.")

# --- Data Table ---
st.write("---")
st.header("Data Table")

display_table_df = filtered_df[['Year', 'Sector', 'Indicator', 'Value', 'Type']].copy()
# Pivot for better display if needed, but keeping it simple for now
# For example, to show indicators as columns:
table_pivot_df = display_table_df.pivot_table(
    index=['Year', 'Sector', 'Type'],
    columns='Indicator',
    values='Value'
).reset_index()

st.dataframe(table_pivot_df.style.format("{:.2f}"))

# --- Download Button ---
st.write("---")
st.header("Download Data")

# Create a CSV for download
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(filtered_df)

st.download_button(
    label="Download Data as CSV",
    data=csv_data,
    file_name=f"Rwanda_Macroeconomic_Data_{selected_sector}_{selected_years[0]}-{selected_years[1]}.csv",
    mime="text/csv",
)

st.caption("Data Source: Simulated for demonstration. In a real scenario, cite your actual data sources (e.g., World Bank, IMF, National Institute of Statistics of Rwanda).")