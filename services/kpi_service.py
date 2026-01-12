import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
sys.path.insert(0, PROJECT_DIR)  # add project root to Python path


from data_loader import load_data
from services.metrics_registry import METRICS_REGISTRY

# Load data once
data = load_data()

#print(data.head())
def get_kpis(sector, subsector, year, decimals=1):
    """
    Returns all KPIs for a given sector & subsector for a specific year
    Output format:
    {
        "KPI label": "formatted value",
        ...
    }
    """

    results = {}

    # Safety checks
    if sector not in METRICS_REGISTRY:
        return results

    if subsector not in METRICS_REGISTRY[sector]:
        return results

    kpi_definitions = METRICS_REGISTRY[sector][subsector]

    for label, (component, unit) in kpi_definitions.items():

        filtered = data.query(
            'sector == @sector and subsector == @subsector '
            'and component == @component and unit == @unit '
            'and year == @year'
        )["value"]

        if not filtered.empty:
            value = filtered.squeeze()
            results[label] = f"{value:.{decimals}f}"
        else:
            results[label] = "N/A"

    return results
