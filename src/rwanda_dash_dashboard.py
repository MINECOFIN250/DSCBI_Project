import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import base64
import io

# --- 1. Data Acquisition & Preparation (Simulated for demonstration) ---
def load_data():
    years = np.arange(2010, 2026) # Up to 2023 historical, 2024-2025 projection
    data = []

    # Simulate GDP Growth (Annual %)
    gdp_growth = np.random.uniform(3, 8, len(years))
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

# Initialize the Dash app
app = dash.Dash(__name__)

# --- 2. Dash App Layout ---
app.layout = html.Div(style={'backgroundColor': '#282a36', 'color': '#f8f8f2', 'fontFamily': 'Arial, sans-serif'}, children=[
    html.H1("RWANDA'S ECONOMY MACROECONOMIC DASHBOARD", style={'textAlign': 'center', 'padding': '20px', 'color': '#8be9fd'}),
    html.H2("Macro-Economic Indicators - Historical & Projections", style={'textAlign': 'center', 'color': '#f1fa8c'}),

    html.Div(className='row', style={'display': 'flex', 'padding': '20px'}, children=[
        # Left Panel (Selection Panel)
        html.Div(className='three columns', style={'flex': 1, 'padding': '20px', 'backgroundColor': '#44475a', 'borderRadius': '8px', 'marginRight': '20px'}, children=[
            html.H3("SELECTION PANEL", style={'color': '#ff79c6'}),

            html.Label("Sector", style={'marginTop': '10px'}),
            dcc.Dropdown(
                id='sector-dropdown',
                options=[{'label': i, 'value': i} for i in all_sectors],
                value=all_sectors[0],
                clearable=False,
                style={'backgroundColor': '#6272a4', 'color': '#f8f8f2'}
            ),

            html.Label("Indicator 1 for Chart", style={'marginTop': '20px'}),
            dcc.Dropdown(
                id='indicator-1-dropdown',
                options=[{'label': i, 'value': i} for i in all_indicators],
                value=all_indicators[0],
                clearable=False,
                style={'backgroundColor': '#6272a4', 'color': '#f8f8f2'}
            ),

            html.Label("Indicator 2 for Chart", style={'marginTop': '20px'}),
            dcc.Dropdown(
                id='indicator-2-dropdown',
                options=[{'label': i, 'value': i} for i in all_indicators],
                value=all_indicators[1],
                clearable=False,
                style={'backgroundColor': '#6272a4', 'color': '#f8f8f2'}
            ),

            html.Label("Year Range", style={'marginTop': '20px'}),
            dcc.RangeSlider(
                id='year-range-slider',
                min=min_year,
                max=max_year,
                step=1,
                value=[min_year, max_year],
                marks={str(year): str(year) for year in range(min_year, max_year + 1, 2)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),

            html.H4("Display Options", style={'marginTop': '30px', 'color': '#bd93f9'}),
            dcc.Checklist(
                id='display-options-checklist',
                options=[
                    {'label': ' Historical Trend', 'value': 'Historical'},
                    {'label': ' Projection', 'value': 'Projection'}
                ],
                value=['Historical', 'Projection'], # Both checked by default
                style={'marginTop': '10px'}
            )
        ]),

        # Right Panel (Charts and Table)
        html.Div(className='nine columns', style={'flex': 3, 'padding': '20px', 'backgroundColor': '#44475a', 'borderRadius': '8px'}, children=[
            html.H3("Historical Trend and Projection", style={'textAlign': 'center', 'color': '#ff79c6'}),
            
            html.Div(className='row', style={'display': 'flex'}, children=[
                html.Div(className='six columns', style={'flex': 1, 'paddingRight': '10px'}, children=[
                    dcc.Graph(id='indicator-1-chart', config={'displayModeBar': False})
                ]),
                html.Div(className='six columns', style={'flex': 1, 'paddingLeft': '10px'}, children=[
                    dcc.Graph(id='indicator-2-chart', config={'displayModeBar': False})
                ])
            ]),

            html.H3("Data Table", style={'textAlign': 'center', 'marginTop': '30px', 'color': '#ff79c6'}),
            html.Div(id='data-table-container', style={'overflowX': 'auto'}),

            html.H3("Download Data", style={'textAlign': 'center', 'marginTop': '30px', 'color': '#ff79c6'}),
            html.Button("Download Data as CSV", id="btn_csv", style={'margin': '10px auto', 'display': 'block', 'backgroundColor': '#50fa7b', 'color': '#282a36', 'border': 'none', 'padding': '10px 20px', 'borderRadius': '5px', 'cursor': 'pointer'}),
            dcc.Download(id="download-dataframe-csv"),

            html.P("Data Source: Simulated for demonstration. In a real scenario, cite your actual data sources (e.g., World Bank, IMF, National Institute of Statistics of Rwanda).", 
                   style={'textAlign': 'center', 'fontSize': '0.8em', 'marginTop': '20px', 'color': '#6272a4'})
        ])
    ])
])

# --- 3. Callbacks for Interactivity ---

@app.callback(
    Output('indicator-1-chart', 'figure'),
    Output('indicator-2-chart', 'figure'),
    Output('data-table-container', 'children'),
    Output('download-dataframe-csv', 'data'),
    Input('sector-dropdown', 'value'),
    Input('indicator-1-dropdown', 'value'),
    Input('indicator-2-dropdown', 'value'),
    Input('year-range-slider', 'value'),
    Input('display-options-checklist', 'value'),
    Input('btn_csv', 'n_clicks') # For triggering download, though data is prepared regardless
)
def update_dashboard(selected_sector, indicator_1, indicator_2, year_range, display_types, n_clicks):
    # Filter data based on selections
    filtered_df = df[
        (df['Sector'] == selected_sector) &
        (df['Year'] >= year_range[0]) &
        (df['Year'] <= year_range[1])
    ]

    # Apply historical/projection filter
    if not display_types: # If nothing is checked
        filtered_df = pd.DataFrame()
    else:
        filtered_df = filtered_df[filtered_df['Type'].isin(display_types)]

    # --- Chart 1 ---
    fig1 = {}
    if not filtered_df.empty and indicator_1 in filtered_df['Indicator'].unique():
        chart_df_1 = filtered_df[filtered_df['Indicator'] == indicator_1]
        fig1 = px.line(chart_df_1, x='Year', y='Value', 
                       title=f'{indicator_1} Over Time',
                       markers=True,
                       color='Type', 
                       color_discrete_map={'Historical': '#8be9fd', 'Projection': '#50fa7b'}) # Dracula Theme colors
        fig1.update_layout(
            plot_bgcolor='#44475a', paper_bgcolor='#44475a',
            font_color='#f8f8f2',
            title_font_color='#f1fa8c',
            xaxis_title_font_color='#6272a4',
            yaxis_title_font_color='#6272a4'
        )
    else:
        fig1 = {
            'data': [],
            'layout': {
                'title': f"No data for {indicator_1}",
                'plot_bgcolor': '#44475a', 'paper_bgcolor': '#44475a', 'font_color': '#f8f8f2'
            }
        }

    # --- Chart 2 ---
    fig2 = {}
    if not filtered_df.empty and indicator_2 in filtered_df['Indicator'].unique():
        chart_df_2 = filtered_df[filtered_df['Indicator'] == indicator_2]
        fig2 = px.bar(chart_df_2, x='Year', y='Value', 
                      title=f'{indicator_2} Over Time',
                      color='Type',
                      color_discrete_map={'Historical': '#ffb86c', 'Projection': '#ff79c6'}) # Dracula Theme colors
        fig2.update_layout(
            plot_bgcolor='#44475a', paper_bgcolor='#44475a',
            font_color='#f8f8f2',
            title_font_color='#f1fa8c',
            xaxis_title_font_color='#6272a4',
            yaxis_title_font_color='#6272a4'
        )
    else:
        fig2 = {
            'data': [],
            'layout': {
                'title': f"No data for {indicator_2}",
                'plot_bgcolor': '#44475a', 'paper_bgcolor': '#44475a', 'font_color': '#f8f8f2'
            }
        }

    # --- Data Table ---
    table_children = []
    download_data = {}
    if not filtered_df.empty:
        table_pivot_df = filtered_df.pivot_table(
            index=['Year', 'Sector', 'Type'],
            columns='Indicator',
            values='Value'
        ).reset_index()
        table_pivot_df.columns.name = None # Remove the 'Indicator' name from columns

        table_children = html.Table(
            # Header
            [html.Thead(html.Tr([html.Th(col) for col in table_pivot_df.columns]))] +
            # Body
            [html.Tbody([
                html.Tr([
                    html.Td(table_pivot_df.iloc[i][col]) for col in table_pivot_df.columns
                ]) for i in range(len(table_pivot_df))
            ])],
            style={
                'borderCollapse': 'collapse', 'width': '100%', 'marginTop': '20px',
                'textAlign': 'center', 'color': '#f8f8f2'
            }
        )
        download_data = dcc.send_data_frame(table_pivot_df.to_csv, "rwanda_macro_data.csv", index=False)
    else:
        table_children = html.P("No data to display in the table with current selections.", style={'textAlign': 'center', 'color': '#6272a4'})


    return fig1, fig2, table_children, download_data

# Run the app
if __name__ == '__main__':
    app.run(debug=True)