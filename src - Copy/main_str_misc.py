# ==============================
# 📦 SECTION 1: IMPORT LIBRARIES
# ==============================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re
from pathlib import Path

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# ==============================
# 📂 FILE PATHS
# ==============================
DIR_DATA = Path(__file__).resolve().parent.parent
FILE = DIR_DATA / "data" / "MacroSEI.csv"
IMAGE = DIR_DATA / "image" / "minecofin.png"

# ==============================
# 🗂️ LOAD & CLEAN DATA
# ==============================
@st.cache_data
def load_and_clean_data(file):
    df = pd.read_csv(file)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.head(66)

    # Melt to long format
    df = df.melt(id_vars=['Sector', 'Indicator'], var_name='Year', value_name='Value')

    # Clean text and numeric columns
    df['Value'] = df['Value'].apply(lambda x: re.sub(r'[,%]', '', str(x)) if isinstance(x, str) else x)
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    df['Year'] = df['Year'].apply(lambda x: re.sub(r'[^0-9]', '', str(x)) if isinstance(x, str) else x)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    df['Sector'] = df['Sector'].astype(str).str.strip().str.title()
    df['Indicator'] = df['Indicator'].astype(str).str.strip().str.title()

    df.dropna(subset=['Value', 'Year'], inplace=True)
    return df

data = load_and_clean_data(FILE)

# ================================================================================================================
# 🎛️ SIDEBAR FILTERS
# ======================================================================================================================
st.markdown("### 🔎 Filters")

# Create a single column for the filter
col1, = st.columns([2])
with col1:
    selected_type = st.selectbox(
        "Period",
        options=["All", "Actual", "Projection"]
    )

# Filter dataframe
df_filtered = data.copy()
if selected_type != "All":
    df_filtered = df_filtered[df_filtered["Data type"] == selected_type]

# Display filtered dataframe
st.dataframe(
    df_filtered,
    use_container_width=True,
    height=450
)


# Multi-select sectors
st.sidebar.header("Filter Options")
sector_options = sorted(data["Sector"].unique())
selected_sector = st.sidebar.selectbox("Select sector", sector_options)
default=[sector_options[5]]  # Select first sector by default

# Multi-select indicators
indicator_options = sorted(
    data[data["Sector"] == selected_sector]["Indicator"].unique())
select_all = st.sidebar.checkbox("Select all indicators", value=False)
if select_all:
    selected_indicators = indicator_options
else:
    selected_indicators = st.sidebar.multiselect(
        "Select indicator",
        options=indicator_options,
        default=[indicator_options[0]]  # Select first indicator by default
    )

# Multi-select years dropdown
year_options = sorted(data["Year"].unique())
select_all = st.sidebar.checkbox("Select all years", value=False)

if select_all:
    selected_years = year_options
else:
    selected_years = st.sidebar.multiselect(
        "Select Year(s)",
        options=year_options,
        default=[min(year_options)]
    )

# ==============================
# 🧭 PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="OCE Macroeconomic Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================================================================
# 🏷️ HEADER
# ==============================================================================================================================
st.image(IMAGE, width=1000)
#st.subheader("📊 Macroeconomic Dashboard")
import streamlit as st

st.markdown(
    """
    <style>
    .dashboard-title {
        color: #002F6C;
        font-size: 42px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<div class='dashboard-title'>📊 Macroeconomic Dashboard</div>",
    unsafe_allow_html=True
)

# ==========================================================================================================================

import pandas as pd
import re

def load_and_clean_data(file, indicators=None):
    df = pd.read_csv(file)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # remove unnamed cols
    df = df.head(66)  # first 66 rows

    # Melt to long format
    df = df.melt(id_vars=['Sector', 'Indicator'], var_name='Year', value_name='Value')

    # Clean numeric columns
    df['Value'] = df['Value'].apply(lambda x: re.sub(r'[,%]', '', str(x)) if isinstance(x, str) else x)
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    # Clean year column
    df['Year'] = df['Year'].apply(lambda x: re.sub(r'[^0-9]', '', str(x)) if isinstance(x, str) else x)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    # Clean text columns
    df['Sector'] = df['Sector'].astype(str).str.strip().str.title()
    df['Indicator'] = df['Indicator'].astype(str).str.strip().str.title()

    df.dropna(subset=['Value', 'Year'], inplace=True)

    # Optional: filter for specific indicators
    if indicators:
        # Normalize indicators: strip, lower case
        df['Indicator_norm'] = df['Indicator'].str.strip().str.lower()
        indicators_norm = [i.strip().lower() for i in indicators]

        # Keep only matching indicators
        df = df[df['Indicator_norm'].isin(indicators_norm)].copy()
        df.drop(columns=['Indicator_norm'], inplace=True)

    return df

# ======================================================================================================================
# 📈 KEY METRICS
# =========================================================================================================================
def compute_key_metrics(df, sector, indicator, years):
    filtered = df[(df['Sector'] == sector) & (df['Indicator'].isin(indicator))]
    if years:
        filtered = filtered[filtered['Year'].isin(years)]

    if filtered.empty:
        return None

    max_value = filtered['Value'].max()
    avg_value = filtered['Value'].mean()
    min_value = filtered['Value'].min()
    long_term_projection = filtered.sort_values('Year')['Value'].iloc[-1]

    return {
        "Max": max_value,
        "Average": avg_value,
        "Min": min_value,
        "Medium-Term Average": long_term_projection
    }

metrics = compute_key_metrics(data, selected_sector, selected_indicators, selected_years)

if metrics:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Minimum", f"{metrics['Min']:.2f}")
    col2.metric("Maximum", f"{metrics['Max']:.2f}")
    col3.metric("Average", f"{metrics['Average']:.2f}")
    col4.metric("Medium-Term Average", f"{metrics['Medium-Term Average']:.2f}")
   
else:
    st.warning("No data available, please select data.")

# ============================================================================================
# 📊 CHARTS
#=============================================================================================

def plot_indicator_charts(df, sector, indicators, years):
    filtered = df[
        (df['Sector'] == sector) &
        (df['Indicator'].isin(indicators)) &
        (df['Year'].isin(years))
    ].sort_values(by=['Indicator', 'Year'])

    if filtered.empty:
        st.warning("No enough information selected, please select more.")
        return

    # --------------------------------------------------------------------------------
    # Trend Chart
    # ---------------------------------------------------------------------------------
    fig_trend = px.line(
        filtered,
        x='Year',
        y='Value',
        color='Indicator',
        markers=True,
        title=f"📈{selected_sector}",
        hover_data={'Value': ':.2f', 'Year': True},
        line_shape='spline',  # smooth lines
        width=900,
        height=500
    )
    fig_trend.update_traces(mode="lines+markers", line = dict(width=3))
    fig_trend.update_layout(
        template='plotly_white',
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        title_font=dict(size=20, color="#1f2c56"),
        #legend=dict(title="Indicator", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(
            title='Year',
            showline=True,          # ensure the x-axis line is visible
            linecolor='black',      # axis line color
            showgrid=True,
            gridcolor='lightgrey',
            tickmode='linear',
            dtick=1,
            tickfont=dict(color='black', size=12)
        ),
        yaxis=dict(
            title='Value',
            showline=True,          # ensure the y-axis line is visible
            linecolor='black',      # axis line color
            showgrid = True,
            gridcolor ='lightgrey',
            tickfont = dict(color='black', size=12)
        ),
        legend=dict(title="Indicator", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    #fig_trend.update_traces(mode="lines+markers", line=dict(width=3), marker=dict(size=8))
    st.plotly_chart(fig_trend, use_container_width=True)

    # -----------------------------------------------------------------------------------------
    # Year-over-Year percentage change(per indicator)
    # --------------------------------------------------------------------------------------------------
    df_yoy = filtered.copy()
    df_yoy['Percentage change(%)'] = df_yoy.groupby('Indicator')['Value'].pct_change() * 100
    df_yoy.dropna(subset=['Percentage change(%)'], inplace=True)

    if not df_yoy.empty:
        fig_growth = px.bar(
            df_yoy,
            x='Year',
            y='Percentage change(%)',
            color='Indicator',
            barmode='group',
            title=f"📊 Growth rate (YoY percentage change)",
            hover_data={'Percentage change(%)': ':.2f', 'Year': True},
            text='Percentage change(%)',
            width=900,
            height=500
        )
        fig_growth.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

        ## Layout adjustments
        fig_trend.update_layout(
            template='plotly_white',
            plot_bgcolor="#f9f9f9",
            paper_bgcolor="#f9f9f9",
            title_font=dict(size=20, color="#1f2c56"),
            
            xaxis=dict(
                title='Year',
                showline=True,          # ensure the x-axis line is visible
                linecolor='black',      # axis line color
                showgrid=True,
                gridcolor='lightgrey',
                tickmode='linear',
                dtick=1,
                tickfont=dict(color='black', size=12)
            ),
            yaxis=dict(
                title='Percentage change(%)',
                showline=True,          # ensure the y-axis line is visible
                linecolor='black',      # axis line color
                showgrid=True,
                gridcolor='lightgrey',
                tickfont=dict(color='black', size=12)
            ),
            legend=dict(title="Indicator", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_growth, use_container_width=True)
    else:
        st.info("Not enough data selected to make the chart, please select more years")

plot_indicator_charts(data, selected_sector, selected_indicators, selected_years)

# =========================================================================================================
# 📊 DISPLAY TABLE FOR MULTI-INDICATORS
# ==============================================================================================================
if selected_indicators and selected_years:
    filtered_table = data[
        (data['Sector'] == selected_sector) &
        (data['Indicator'].isin(selected_indicators)) &
        (data['Year'].isin(selected_years))]
    if not filtered_table.empty:
        # Pivot to get indicators as rows and years as columns
        table_display = filtered_table.pivot(index='Indicator', columns='Year', values='Value')
        st.subheader(f"📈{selected_sector}")
        st.dataframe(table_display.style.format("{:.2f}"))
    else:
        st.warning("Not enough data selected to make the table, please select more data")

# 🚀 SECTION 10: RUN THE APP
# Streamlit entry point for running the dashboard application.
# ==============================
if __name__ == "__main__":
    st.write("Macroeconomic Dashboard is running...")