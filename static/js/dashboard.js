// ================= GLOBAL STATE =================
let selectedSector = null;
let selectedSubsector = null;
let selectedComponent = null;
let selectedUnit = null;
let selectedYear = null;
let selectedType = "actual";
let componentChart = null;
let chartType = "line";

// ================= LOAD YEARS =================
async function loadYears(type = selectedType) {
    const res = await fetch("/api/years");
    const data = await res.json();
    const yearSelect = document.getElementById("year-select");
    yearSelect.innerHTML = "";

    const years = type === "actual" ? data.actual : data.projection;
    years.forEach(y => {
        const opt = document.createElement("option");
        opt.value = y;
        opt.textContent = y;
        yearSelect.appendChild(opt);
    });

    selectedYear = yearSelect.value;

    yearSelect.onchange = () => {
        selectedYear = yearSelect.value;
        if (selectedSector && selectedSubsector) loadKPIs(selectedSector, selectedSubsector, selectedYear);
        if (selectedSector && selectedSubsector && selectedComponent && selectedUnit) loadComponentKPI();
        if (selectedSector && selectedSubsector && selectedComponent && selectedUnit) loadChart();
    };
}

// ================= LOAD KPI CARDS =================
async function loadKPIs(sector, subsector, year) {
    const container = document.getElementById("kpi-cards-container");
    container.innerHTML = "<p>Loading KPIs...</p>";

    const res = await fetch(`/api/kpis/${encodeURIComponent(sector)}/${encodeURIComponent(subsector)}/${year}`);
    const kpis = await res.json();

    container.innerHTML = "";
    Object.entries(kpis).forEach(([label, value]) => {
        const card = document.createElement("div");
        card.className = "kpi-card";
        card.innerHTML = `<h4>${label}</h4><p>${value}</p>`;
        container.appendChild(card);
    });
}

// ================= LOAD SUBSECTORS =================
async function loadSubsectors(sector) {
    selectedSector = sector;
    selectedSubsector = null;

    const res = await fetch(`/api/subsectors/${encodeURIComponent(sector)}`);
    const subsectors = await res.json();

    const container = document.getElementById("subsector-container");
    container.innerHTML = "";

    subsectors.forEach(sub => {
        const btn = document.createElement("button");
        btn.className = "subsector-btn";
        btn.textContent = sub;

        btn.onclick = () => {
            document.querySelectorAll(".subsector-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            selectedSubsector = sub;
            document.getElementById("selected-subsector-title").textContent = sub;
            loadKPIs(sector, sub, selectedYear);
            loadComponents(sector, sub);
        };

        container.appendChild(btn);
    });

    if (subsectors.length) container.querySelector("button").click();
}

// ================= LOAD COMPONENTS =================
async function loadComponents(sector, subsector) {
    selectedComponent = null;
    const res = await fetch(`/api/components/${encodeURIComponent(sector)}/${encodeURIComponent(subsector)}`);
    const components = await res.json();

    const container = document.getElementById("component-container");
    container.innerHTML = "";

    components.forEach(comp => {
        const btn = document.createElement("button");
        btn.className = "component-btn";
        btn.textContent = comp;

        btn.onclick = () => {
            document.querySelectorAll(".component-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            selectedComponent = comp;
            document.getElementById("component-title").textContent = selectedComponent;
            loadUnits(sector, subsector, comp);
        };

        container.appendChild(btn);
    });

    if (components.length) container.querySelector("button").click();
}

// ================= LOAD UNITS =================
async function loadUnits(sector, subsector, component) {
    const select = document.getElementById("unit-select");
    select.innerHTML = "<option>Loading...</option>";

    const res = await fetch(`/api/units/${encodeURIComponent(sector)}/${encodeURIComponent(subsector)}/${encodeURIComponent(component)}`);
    const units = await res.json();

    select.innerHTML = "";
    units.forEach(u => {
        const opt = document.createElement("option");
        opt.value = u;
        opt.textContent = u;
        select.appendChild(opt);
    });

    selectedUnit = select.value;

    select.onchange = () => {
        selectedUnit = select.value;
        loadComponentKPI();
        loadChart();
    };

    loadComponentKPI();
    loadChart();
}

// ================= LOAD COMPONENT KPI =================
async function loadComponentKPI() {
    if (!selectedComponent || !selectedUnit) return;
    const card = document.getElementById("component-kpi-card");
    card.innerHTML = "<p>Loading...</p>";

    const res = await fetch(`/api/kpis/${encodeURIComponent(selectedSector)}/${encodeURIComponent(selectedSubsector)}/${selectedYear}`);
    const kpis = await res.json();
    const entry = Object.entries(kpis).find(([k]) => k.includes(selectedComponent));
    card.innerHTML = entry ? `<h4>${selectedComponent} (${selectedUnit})</h4><p>${entry[1]}</p>` : "<p>N/A</p>";
}

// ================= LOAD CHART =================
async function loadChart() {
    if (!selectedComponent || !selectedUnit) return;
    const ctx = document.getElementById("component-chart");

    const yearsRes = await fetch("/api/years");
    const yearsData = await yearsRes.json();

    const actualYears = yearsData.actual;
    const projYears = yearsData.projection;

    async function fetchSeries(years) {
        const vals = [];
        for (let y of years) {
            const res = await fetch(`/api/kpis/${encodeURIComponent(selectedSector)}/${encodeURIComponent(selectedSubsector)}/${y}`);
            const kpis = await res.json();
            const found = Object.entries(kpis).find(([k]) => k.includes(selectedComponent));
            vals.push(found ? parseFloat(found[1]) : null);
        }
        return vals;
    }

    const actualValues = await fetchSeries(actualYears);
    const projectionValues = await fetchSeries(projYears);

    if (componentChart) componentChart.destroy();

    componentChart = new Chart(ctx, {
        type: chartType,
        data: {
            labels: [...actualYears, ...projYears],
            datasets: [
                {
                    label: "Actual",
                    data: actualValues,
                    borderColor: "#0366d6",
                    backgroundColor: chartType === "line" ? "transparent" : "#0366d6",
                    borderWidth: 2
                },
                {
                    label: "Projection",
                    data: Array(actualYears.length).fill(null).concat(projectionValues),
                    borderColor: "#d66a03",
                    backgroundColor: chartType === "line" ? "transparent" : "#d66a03",
                    borderDash: [6,6],
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            interaction: { mode: "index", intersect: false }
        }
    });
}

// ================= CHART TYPE BUTTONS =================
document.getElementById("line-btn").onclick = () => { chartType="line"; loadChart(); };
document.getElementById("column-btn").onclick = () => { chartType="bar"; loadChart(); };

// ================= SIDEBAR TOGGLE =================
document.getElementById("sidebar-toggle").onclick = () => document.querySelector(".sidebar").classList.toggle("collapsed");

// ================= INIT DASHBOARD =================
async function initDashboard() {
    await loadYears();

    const res = await fetch("/api/sectors");
    const sectors = await res.json();

    document.querySelectorAll(".sidebar-btn[data-sector]").forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll(".sidebar-btn[data-sector]").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            const title = document.getElementById("selected-sector-title");
            if (title) title.textContent = btn.dataset.sector;
            loadSubsectors(btn.dataset.sector);
        };
    });

    if (sectors.length) document.querySelector(`.sidebar-btn[data-sector='${sectors[0]}']`)?.click();
}

document.addEventListener("DOMContentLoaded", initDashboard);
