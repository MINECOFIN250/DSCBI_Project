# This file defines ALL KPIs available in the dashboard
# Structure:
# Sector → Subsector → KPI Label → (Component, Unit)

METRICS_REGISTRY = {

    # =========================
    # REAL SECTOR
    # =========================
    "Real sector": {

        "GDP and components": {
            "Real GDP (billion FRW)": (
                "Real GDP",
                "Billion RWF, Level"
            ),
            "Public investment (% GDP)": (
                "Government investment",
                "Percentage of GDP"
            ),
            "Private investment (% GDP)": (
                "Private Investment",
                "Percentage of GDP"
            ),
        },

        "Inflation and other prices": {
            "Inflation (eop)": (
                "Consumer Price Index",
                "CPI, Percentage, eop"
            ),
            "Inflation (pa)": (
                "Consumer Price Index",
                "CPI, Percentage, pa"
            ),
            "GDP Deflator": (
                "GDP deflator",
                "Percentage"
            ),
        },
    },

    # =========================
    # FISCAL SECTOR
    # =========================
    "Fiscal sector": {

        "Revenue": {
            "Revenue (% GDP)": (
                "Revenues incl. grants",
                "Percentage of GDP"
            ),
            "Tax revenue (% GDP)": (
                "Tax revenue",
                "Percentage of GDP"
            ),
            "Grants (% GDP)": (
                "Grants",
                "Percentage of GDP"
            ),
        },

        "Expenditure": {
            "Expenditures (% GDP)": (
                "Expenditure",
                "Percentage of GDP"
            ),
            "Expense (% GDP)": (
                "Expense",
                "Percentage of GDP"
            ),
        },

        "Fiscal balance": {
            "Fiscal balance (inc. grants, % GDP)": (
                "Fiscal Balance/Deficit",
                "Percentage of GDP"
            ),
            "Fiscal balance (excl. grants, % GDP)": (
                "Fiscal Balance/Deficit",
                "Exl, grants, Percentage of GDP"
            ),
        },
    },

    # =========================
    # EXTERNAL SECTOR
    # =========================
    "External sector": {

        "Exports": {
            "Exports of goods & services (% GDP)": (
                "Exports of goods & services",
                "Percentage of GDP"
            ),
        },

        "Imports": {
            "Imports of goods & services (% GDP)": (
                "Imports of goods & services",
                "Percentage of GDP"
            ),
        },

        "Trade balance": {
            "Trade balance (% GDP)": (
                "Trade balance",
                "Percentage of GDP"
            ),
        },

        "FDI": {
            "FDI (% GDP)": (
                "Foreign Direct Investment",
                "FDI, Percetantage of GDP"
            ),
        },

        "Reserves": {
            "Reserves (Months of imports)": (
                "Gross official reserves",
                "Million USD, Months of imports"
            ),
        },

        "Current Account Balance": {
            "Current Account Balance (% GDP)": (
                "Current Account Balance",
                "Percentage of GDP"
            ),
        },
    },

    # =========================
    # MONETARY SECTOR
    # =========================
    "Monetary sector": {

        "Broad money": {
            "Broad money (M3)": (
                "Broad Money",
                "M3, Million USD, Level"
            ),
        },

        "Credit to private Sector": {
            "Credit to private Sector (M3)": (
                "Credit Private Sector",
                "CPS Million USD, Level"
            ),
        },

        "Credit to Govt": {
            "Credit to Govt": (
                "Credit Government",
                "CG, Million USD, Level"
            ),
        },

        "Exchange rate": {
            "Exchange rate (FRW/US$)": (
                "Exchange rate",
                "RWF/USD"
            ),
            "Exchange rate (Y-0-Y)":(
                "Exchange rate",
                "RWF/USD, Percentage change"
            ),
            
        },


    },
}
