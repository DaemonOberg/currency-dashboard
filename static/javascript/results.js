
/* ========================================
   1. CHART ELEMENTS
   Get chart elements from the HTML
======================================== */

const switchButton = document.getElementById("switch-chart");
const lineChart = document.getElementById("line-chart");
const barChart = document.getElementById("bar-chart");
const periodControl = document.getElementById("period-control");

/* ========================================
   2. CHART SWITCHING
   Switch between line and bar charts
======================================== */

switchButton.addEventListener("click", function() {
    if (getComputedStyle(lineChart).display === "none") {
        lineChart.style.display = "block";
        barChart.style.display = "none";
        periodControl.style.display = "flex";

        /* Resize the line chart after it becomes visible */
        requestAnimationFrame(() => {
            Plotly.Plots.resize(lineChart.querySelector(".js-plotly-plot"));
        });
    } else {
        lineChart.style.display = "none";
        barChart.style.display = "block";
        periodControl.style.display = "none";

        /* Resize the bar chart after it becomes visible */
        requestAnimationFrame(() => {
            Plotly.Plots.resize(barChart.querySelector(".js-plotly-plot"));
        });
    }
});

/* ========================================
   3. PERIOD SELECTION
   Update chart data when the period changes
======================================== */

const periodSelect = document.getElementById("period-select");

periodSelect.addEventListener("change", function() {
    // Get the selected time period
    const selectedPeriod = periodSelect.value;

    // Read selected currencies and SEK amount from the URL
    const currencies = new URLSearchParams(window.location.search).getAll("currencies");
    const amount = Number(new URLSearchParams(window.location.search).get("amount"));
    const url = `/api/chart?period=${selectedPeriod}&${currencies.map(currency => `currencies=${currency}`).join("&")}`;

    /* Fetch updated exchange rates from Flask */
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Could not retrieve historical exchange rates.");
            }
            return response.json();
        })
        .then(data => {
            const records = data.records;
            const plotElement = lineChart.querySelector(".js-plotly-plot");

            /* Prepare dates for each currency */
            const newX = plotElement.data.map(trace => {
                const currency = trace.name.split(" to ").pop();
                return records
                    .filter(record => record.currency === currency)
                    .map(record => record.date);
            });

            /* Calculate converted SEK amounts for each currency */
            const newY = plotElement.data.map(trace => {
                const currency = trace.name.split(" to ").pop();
                return records
                    .filter(record => record.currency === currency)
                    .map(record => record.sek * amount);
            });

            /* Update Plotly chart values */
            Plotly.restyle(plotElement, {
                x: newX,
                y: newY
            });

            /* Adjust the number of date ticks */
            Plotly.relayout(plotElement, {
                "xaxis.nticks": 12
            });
        })

        /* Handle API and network errors */
        .catch(error => {
            alert(error.message);
        });
});
