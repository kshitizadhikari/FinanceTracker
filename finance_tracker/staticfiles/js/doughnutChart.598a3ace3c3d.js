import { makeGetRequest } from "./utils.js";

let doughnutChartInstance = null;

export default function renderChart(chartName, url) {
    let labelData = [];
    let datasetData = [];

    const fetchDataAndRenderChart = async () => {
        try {
            const data = await makeGetRequest(url);

            if (data) {
                for (let item in data) {
                    labelData.push(item);
                    datasetData.push(data[item]);
                }

                const ctx = $("#doughnut")[0].getContext("2d"); // Use jQuery to get the canvas context

                if (doughnutChartInstance) {
                    doughnutChartInstance.destroy();
                }

                doughnutChartInstance = new Chart(ctx, {
                    type: "doughnut",
                    data: {
                        labels: labelData,
                        datasets: [
                            {
                                label: chartName,
                                data: datasetData,
                                hoverOffset: 4,
                            },
                        ],
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
