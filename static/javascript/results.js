const switchButton = document.getElementById("switch-chart");
const lineChart = document.getElementById("line-chart");
const barChart = document.getElementById("bar-chart");
switchButton.addEventListener("click", function() {
    if (getComputedStyle(lineChart).display === "none") {
        lineChart.style.display = "block";
        barChart.style.display = "none";
    } else {
        lineChart.style.display = "none";
        barChart.style.display = "block";
    }
});

const periodSelect = document.getElementById("period-select");
periodSelect.addEventListener("change", function() {
    const selectedPeriod = periodSelect.value;
    const currencies = new URLSearchParams(window.location.search).getAll("currencies");
    const amount = Number(new URLSearchParams(window.location.search).get("amount"));
    const url = `/api/chart?period=${selectedPeriod}&${currencies.map(currency => `currencies=${currency}`).join("&")}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const records = data.records;
            const plotElement = lineChart.querySelector(".js-plotly-plot");

            const newX = plotElement.data.map(trace => {
                const currency = trace.name.split(" to ").pop();
                return records
                    .filter(record => record.currency === currency)
                    .map(record => record.date);
            });

            const newY = plotElement.data.map(trace => {
                const currency = trace.name.split(" to ").pop();
                return records
                    .filter(record => record.currency === currency)
                    .map(record => record.sek * amount);
            });

            Plotly.restyle(plotElement, {
                x: newX,
                y: newY
            });
Plotly.relayout(plotElement, {
    "xaxis.nticks": 12
});
});
});
