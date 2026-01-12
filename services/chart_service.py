from data_loader import load_data

data = load_data()

def get_chart_data(sector, subsector, component, unit, data_type, cutoff=2025):
    """
    Returns time-series data for charts
    """

    df = data[
        (data["sector"] == sector) &
        (data["subsector"] == subsector) &
        (data["component"] == component) &
        (data["unit"] == unit)
    ].sort_values("year")

    if data_type == "actual":
        df = df[df["year"] <= cutoff]
    else:
        df = df[df["year"] > cutoff]

    return {
        "years": df["year"].tolist(),
        "values": df["value"].tolist(),
        "type": data_type
    }
