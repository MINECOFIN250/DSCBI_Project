
import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, PROJECT_DIR)  # add project root to Python path


from flask import Flask, render_template, jsonify
from services.data_service import get_sectors, get_subsectors, get_components, get_years, get_units
from services.kpi_service import get_kpis
from services.chart_service import get_chart_data


# =======================
# Paths
# =======================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "..", "templates"),
    static_folder=os.path.join(BASE_DIR, "..", "static")
)

# =======================
# ROUTES
# =======================

# --- Dashboard HTML ---
@app.route("/")
def dashboard():
    """
    Render the main dashboard page
    """
    years_dict = get_years()
    return render_template(
        "dashboard.html",
        sectors=get_sectors(),
        actual_years=years_dict["actual"],
        projection_years=years_dict["projection"]
    )


# --- API Endpoints ---

@app.route("/api/sectors")
def api_sectors():
    return jsonify(get_sectors())


@app.route("/api/subsectors/<sector>")
def api_subsectors(sector):
    return jsonify(get_subsectors(sector))


@app.route("/api/components/<sector>/<subsector>")
def api_components(sector, subsector):
    return jsonify(get_components(sector, subsector))


@app.route("/api/units/<sector>/<subsector>/<component>")
def api_units(sector, subsector, component):
    return jsonify(get_units(sector, subsector, component))



@app.route("/api/years")
def api_years():
    return jsonify(get_years())

@app.route("/api/chart/<sector>/<subsector>/<component>/<unit>/<data_type>")
def api_chart_data(sector, subsector, component, unit, data_type):
    return jsonify(
        get_chart_data(
            sector=sector,
            subsector=subsector,
            component=component,
            unit=unit,
            data_type=data_type
        )
    )





@app.route("/api/kpis/<sector>/<subsector>/<int:year>")
def api_kpis(sector, subsector, year):
    """
    Return KPI cards for a given sector, subsector, and year
    """
    return jsonify(get_kpis(sector, subsector, year))


# =======================
# RUN APP
# =======================
if __name__ == "__main__":
    app.run(debug=True)



#from flask import Flask, render_template
# import pandas as pd
# from data_loader import load_data
#import os

# #====================================================================================
# #loading data
# data = load_data()

# sectors = list(data["sector"].unique())

# #df sectors
# sectors = list([n for n in sectors if n not in ['Debt sector','Other memo items']])

# #df subsectors
# subsectors = list(
#     data[data["sector"].isin(sectors)]["subsector"]
# )
# #df components
# components = data[
#     data["sector"].isin(sectors) &
#     data["subsector"].isin(subsectors)
# ]["component"].unique().tolist()

# #df units
# units = data[
#     data["sector"].isin(sectors) &
#     data["subsector"].isin(subsectors) & data["component"].isin(components)
# ]["unit"].unique().tolist()

# #df units
# years = data["year"].unique().tolist()
# Actual = [n for n in years if n <= 2025]
# projection = [n for n in years if n > 2025]


# #=========================================================================
# # a function which retrieves key metrics
# def get_value(df, sector, subsector, component, unit, year):

#     filtered = data.query(
#         'sector == @sector and subsector == @subsector and component == @component and unit == @unit and year == @year'
#     )["value"]

#     if not filtered.empty:
#         return filtered.squeeze()  # returns scalar if single value
#     else:
#         return None
    



# def get_fmt(df, sector, subsector, component, unit, year, decimals=1):
#     val = get_value(df, sector, subsector, component, unit, year)
#     return f"{val:.{decimals}f}" if val is not None else "N/A"




# #=====================================================================
# REAL_SECTOR = sectors[0]
# FISCAL_SECTOR = sectors[2]
# EXTERNAL_SECTOR = sectors[1]
# MONETARY_SECTOR = sectors[3]
# YEAR = 2025

# metrics = {
#     "Real GDP  (billion FRW)": ("GDP and components", "Real GDP", "Billion RWF, Level"),
#     "Public investment (% GDP)": ("GDP and components", "Government investment", "Percentage of GDP"),
#     "Private investment (% GDP)": ("GDP and components", "Private Investment", "Percentage of GDP"),
#     "Inflation (eop)": ("Inflation and other prices", "Consumer Price Index", "CPI, Percentage, eop"),
#     "Inflation (pa)": ("Inflation and other prices", "Consumer Price Index", "CPI, Percentage, pa"),
#     "GDP Deflator": ("Inflation and other prices", "GDP deflator", "Percentage"),

#     #Fiscal sector
#     "Revenue (% GDP)": ("Revenue","Revenues incl. grants",	"Percentage of GDP"),
#     "Tax revenue (% GDP)": ("Revenue", "Tax revenue","Percentage of GDP"),
#     "Grants (% GDP)": ("Revenue", "Grants",	"Percentage of GDP"),
#     "Expenditures (% GDP)":("Expenditure", "Expenditure", "Percentage of GDP"),
#     "Expense (% GDP)":("Expenditure", "Expense", "Percentage of GDP"),	
#     "Fiscal balance (inc. grants, % GDP)": ("Fiscal balance","Fiscal Balance/Deficit", "Percentage of GDP"),
#     "Fiscal balance (inc. grants, % GDP)": ("Fiscal balance","Fiscal Balance/Deficit", "Exl, grants, Percentage of GDP"),

#     #External sector
#     "Exports of goods & services (% GDP)": ("Exports","Exports of goods & services", "Percentage of GDP"),
#     "Imports of goods & services (% GDP)": ("Imports","Imports of goods & services", "Percentage of GDP"),
#     "Trade balance (% GDP)": ("Trade balance","Trade balance", "Percentage of GDP"),
#     "FDI (% GDP)": ("FDI","Foreign Direct Investment", "FDI, Percetantage of GDP"),
#     "Reserves (Months of imports)": ("Reserves","Gross official reserves", "Million USD, Months of imports"),
#     "Current Account Balance (% GDP)": ("Current Account Balance","Current Account Balance", "Percentage of GDP"),

#     #Monetary sector
#     "Broad money (M3)": ("Broad money","Broad Money", "M3, Million USD,Level"),
#     "Credit to private Sector (M3)": ("Credit Private Sector","Credit Private Sector", "CPS Million USD, Level"),
#     "Credit to Govt": ("Credit to Govt","Credit Government", "CG, Million USD, Level"),
#     "Exchange rate (FRW/US$)": ("Exchange rate","Exchange rate", "RWF/USD")
		
# }		
		
# real_sector = {
#     label: get_fmt(data, REAL_SECTOR, sub, comp, unit, YEAR)
#     for label, (sub, comp, unit) in metrics.items()
# }
# fiscal_sector = {
#     label: get_fmt(data, FISCAL_SECTOR, sub, comp, unit, YEAR)
#     for label, (sub, comp, unit) in metrics.items()
# }
# external_sector = {
#     label: get_fmt(data, EXTERNAL_SECTOR, sub, comp, unit, YEAR)
#     for label, (sub, comp, unit) in metrics.items()
# }
# monetary_sector = {
#     label: get_fmt(data, MONETARY_SECTOR, sub, comp, unit, YEAR)
#     for label, (sub, comp, unit) in metrics.items()
# }
# #print(monetary_sector["Exchange rate (FRW/US$)"])

# #========================================================================================
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# app = Flask(
#     __name__,
#     template_folder=os.path.join(BASE_DIR, "..", "templates"),
#     static_folder=os.path.join(BASE_DIR, "..", "static")
# )

# @app.route("/")
# def dashboard():
#     return render_template(
#         "dashboard.html",
#         sectors=sectors,
#         actual_years=Actual,
#         projection_years=projection
#     )

