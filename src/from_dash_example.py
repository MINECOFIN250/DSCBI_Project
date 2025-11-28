from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd


df = pd.read_csv("C:\\Users\\andrew.mushokambere\\Documents\\DSCBI\\DSCBI_Project\\data\\data.csv")

# Melt the dataframe from wide to long format
df = df.melt(
    id_vars=["Sector", "Indicator", "Desc"],
    var_name="Year",
    value_name="Value"
)

# Ensure Year is numeric
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
app = Dash(__name__)
# server = app.server  # for deployment

# Sidebar layout
sidebar = html.Div(
    [
        html.H2("Macro Dashboard", style={"textAlign": "center"}),
        html.Hr(),
        html.P("Filters:", className="lead"),
        dcc.Dropdown(
            id="Sector-dropdown",
            options=[{"label": i, "value": i} for i in df['Sector'].unique()],
            multi=True,
            placeholder="Select Sector"
        ),
        dcc.Dropdown(
            id="Indicator-dropdown",
            options=[{"label": i, "value": i} for i in df['Indicator'].unique()],
            multi=True,
            placeholder="Select Indicator"
        ),
        dcc.Dropdown(
            id="Year-dropdown",
            options=[{"label": i, "value": i} for i in df['Year'].unique()],
            multi=True,
            placeholder="Select Year"
        ),
    ],
    style={"width": "20%", "display": "inline-block", "verticalAlign": "top", "padding": "20px", "backgroundColor": "#f8f9fa"}
)

# Main content
content = html.Div(
    [
        # KPIs
        html.Div(id="kpi-container", style={"display": "flex", "justifyContent": "space-around", "padding": "20px"}),
        
        # Charts
        dcc.Tabs(
            id="tabs",
            value="tab-RealGDP",
            children=[
                dcc.Tab(label="RealGDP", value="tab-RealGDP"),
                dcc.Tab(label="RealGDPMax", value="tab-RealGDPMax"),
            ],
        ),
        html.Div(id="tabs-content")
    ],
    style={"width": "75%", "display": "inline-block", "padding": "20px", "verticalAlign": "top"}
)

app.layout = html.Div([sidebar, content])


#=====================================================================================================

from dash import Input, Output

@app.callback(
    Output("kpi-container", "children"),
    Input("Sector-dropdown", "value"),
    Input("Indicator-dropdown", "value"),
    Input("Year-dropdown", "value")
)
def update_kpis(selected_sectors, selected_indicators, selected_years):
    dff = df.copy()
    if selected_sectors:
        dff = dff[dff['Sector'].isin(selected_sectors)]
    if selected_indicators:
        dff = dff[dff['Indicator'].isin(selected_indicators)]
    if selected_years:
        dff = dff[dff['Year'].isin(selected_years)]

    kpi1 = html.Div([
        html.H4("Total Depositors"),
        html.P(f"{dff['value'].sum():,}")
    ])
    
    kpi2 = html.Div([
        html.H4("Total Savings"),
        html.P(f"{dff['value'].mean():,}")
    ])
    
    
    return [kpi1, kpi2]

#=====================================================================================================


@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value"),
    Input("Sector-dropdown", "value"),
    Input("Indicator-dropdown", "value"),
    Input("Year-dropdown", "value")
)
def update_tab(tab, selected_sectors, selected_indicators, selected_years):
    dff = df.copy()
    if selected_sectors:
        dff = dff[dff['Sector'].isin(selected_sectors)]
    if selected_indicators:
        dff = dff[dff['Indicator'].isin(selected_indicators)]
    if selected_years:
        dff = dff[dff['Year'].isin(selected_years)]

    if tab == "tab-depositors":
        fig = px.bar(dff, x="District", y="Depositors", color="Institution_Type", barmode="group")
    elif tab == "tab-savings":
        fig = px.bar(dff, x="District", y="Savings", color="Institution_Type", barmode="group")
    elif tab == "tab-credit":
        fig = px.bar(dff, x="District", y="Credit", color="Institution_Type", barmode="group")
    elif tab == "tab-gdp":
        fig = px.line(dff, x="Year", y="GDP", color="District")
    
    return dcc.Graph(figure=fig)

#=========================================================================================
# 5. Run the app
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)