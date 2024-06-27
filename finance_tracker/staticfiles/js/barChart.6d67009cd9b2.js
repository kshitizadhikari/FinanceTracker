import { makeGetRequest } from "./utils.js";

let barChartInstance = null;

export default function renderChart(chartName, url) {
    let labelData = [];
    let datasetData = [];

    const fetchDataAndRenderChart = async () => {
        try {
            const data = await makeGetRequest(url);

            if (data) {
                // Clear previous data
                labelData = [];
                datasetData = [];

                for (let item in data) {
                    labelData.push(item);
                    datasetData.push({
                        label: item,
                        data: [data[item]],
                        borderWidth: 1,
                    });
                }

                const ctx = $("#barChart")[0].getContext("2d");

                // Destroy existing chart instance if it exists
                if (barChartInstance) {
                    barChartInstance.destroy();
                }

                // Create a new chart instance
                barChartInstance = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: [chartName],
                        datasets: datasetData,
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                            },
                        },
                    },
                });
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    // Automatically fetch data and render chart on script load
    fetchDataAndRenderChart();
}
