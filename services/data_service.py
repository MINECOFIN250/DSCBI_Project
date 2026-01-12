from data_loader import load_data

data = load_data()

EXCLUDED_SECTORS = ['Debt sector', 'Other memo items']

def get_sectors():
    sectors = data["sector"].unique().tolist()
    return [s for s in sectors if s not in EXCLUDED_SECTORS]

def get_subsectors(sector):
    return (
        data[data["sector"] == sector]["subsector"]
        .unique()
        .tolist()
    )

def get_components(sector, subsector):
    return (
        data[
            (data["sector"] == sector) &
            (data["subsector"] == subsector)
        ]["component"]
        .unique()
        .tolist()
    )

def get_years(cutoff=2025):
    years = sorted(data["year"].unique().tolist())
    return {
        "actual": [y for y in years if y <= cutoff],
        "projection": [y for y in years if y > cutoff]
    }

def get_units(sector, subsector, component):
    return (
        data[
            (data["sector"] == sector) &
            (data["subsector"] == subsector) &
            (data["component"] == component)
        ]["unit"]
        .unique()
        .tolist()
    )
#print(get_units("Real Sector", "GDP and components","Nominal GDP"))