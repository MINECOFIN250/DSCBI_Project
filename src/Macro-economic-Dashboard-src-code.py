# ===============================================
# RWANDA MACROECONOMIC INDICATORS DASHBOARD
# ===============================================
# Author: Drew
# Description: Interactive Dash app for visualizing Rwanda's macroeconomic data
# ===============================================

import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

# --------------------------
# 1. Load and prepare data
# --------------------------
# Replace this with the path to your actual CSV file
df = pd.read_csv("C:\\Users\\andrew.mushokambere\\Documents\\DSCBI\\DSCBI_Project\\data\\data.csv")

# Melt the dataframe from wide to long format
df_melted = df.melt(
    id_vars=["Sector", "Indicator", "Description"],
    var_name="Year",
    value_name="Value"
)

# Ensure Year is numeric
df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors="coerce")

# --------------------------
# 2. Initialize Dash app
# --------------------------
app = Dash(__name__)
app.title = "Rwanda Macroeconomic Dashboard"

# --------------------------
# 3. App Layout
# --------------------------
app.layout = html.Div([
    html.H1("🇷🇼 Rwanda Macroeconomic Indicators Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Sector:"),
        dcc.Dropdown(
            id="sector-dropdown",
            options=[{"label": s, "value": s} for s in sorted(df_melted["Sector"].unique())],
            value=df_melted["Sector"].unique()[0],
            clearable=False,
            style={"width": "60%"}
        ),

        html.Br(),

        html.Label("Select Indicator:"),
        dcc.Dropdown(
            id="indicator-dropdown",
            options=[],
            value=None,
            clearable=False,
            style={"width": "60%"}
        ),
    ], style={"textAlign": "center"}),

    html.Br(),

    dcc.Graph(id="indicator-chart"),

    html.Br(),

    html.H4("Indicator Data Table", style={"textAlign": "center"}),

    dash_table.DataTable(
        id="data-table",
        columns=[
            {"name": "Year", "id": "Year"},
            {"name": "Value", "id": "Value"}
        ],
        style_table={"width": "60%", "margin": "0 auto"},
        style_cell={"textAlign": "center"},
        style_header={"backgroundColor": "#f2f2f2", "fontWeight": "bold"}
    )
])

# --------------------------
# 4. Callbacks
# --------------------------
@app.callback(
    Output("indicator-dropdown", "options"),
    Output("indicator-dropdown", "value"),
    Input("sector-dropdown", "value")
)
def update_indicator_dropdown(selected_sector):
    indicators = df_melted[df_melted["Sector"] == selected_sector]["Indicator"].unique()
    options = [{"label": i, "value": i} for i in indicators]
    return options, indicators[0]


@app.callback(
    Output("indicator-chart", "figure"),
    Output("data-table", "data"),
    Input("sector-dropdown", "value"),
    Input("indicator-dropdown", "value")
)
def update_chart(selected_sector, selected_indicator):
    filtered = df_melted[
        (df_melted["Sector"] == selected_sector) &
        (df_melted["Indicator"] == selected_indicator)
    ].sort_values("Year")

    fig = px.line(
        filtered,
        x="Year",
        y="Value",
        markers=True,
        title=f"{selected_indicator} ({selected_sector})",
        labels={"Value": "Value", "Year": "Year"}
    )

    fig.update_layout(
        title_x=0.5,
        title_font=dict(size=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True)
    )

    return fig, filtered[["Year", "Value"]].to_dict("records")


# --------------------------
# 5. Run the app
# --------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
