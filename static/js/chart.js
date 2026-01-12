// ================================
// GLOBAL CHART STATE
// ================================
let macroChart = null;
let chartType = "line";   // line | bar
let showProjection = false;

// ================================
// CREATE / UPDATE CHART
// ================================
async function renderChart(sector, subsector, component, unit) {
    if (!sector || !subsector || !component || !unit) return;

    const ctx = document.getElementById("component-chart").getContext("2d");

    // Fetch time series data
    const res = await fetch(
        `/api/chart-data/${encodeURIComponent(sector)}/${encodeURIComponent(subsector)}/${encodeURIComponent(component)}/${encodeURIComponent(unit)}`
    );
    const data = await res.json();

    const labels = data.actual.years;
    const datasets = [];

    // ===== Actual data =====
    datasets.push({
        label: "Actual",
        data: data.actual.values,
        borderWidth: 2,
        tension: 0.4
    });

    // ===== Projection data =====
    if (showProjection && data.projection.values.length > 0) {
        datasets.push({
            label: "Projection",
            data: data.projection.values,
            borderDash: [6, 6],   // dashed line
            borderWidth: 2,
            tension: 0.4
        });
    }

    // Destroy old chart
    if (macroChart) {
        macroChart.destroy();
    }

    // Create chart
    macroChart = new Chart(ctx, {
        type: chartType,
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: "index",
                intersect: false
            },
            plugins: {
                legend: {
                    position: "top"
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// ================================
// CHART TYPE BUTTONS
// ================================
document.getElementById("line-btn").addEventListener("click", () => {
    chartType = "line";
    document.getElementById("line-btn").classList.add("active");
    document.getElementById("column-btn").classList.remove("active");

    renderChart(selectedSector, selectedSubsector, selectedComponent, selectedUnit);
});

document.getElementById("column-btn").addEventListener("click", () => {
    chartType = "bar";
    document.getElementById("column-btn").classList.add("active");
    document.getElementById("line-btn").classList.remove("active");

    renderChart(selectedSector, selectedSubsector, selectedComponent, selectedUnit);
});
