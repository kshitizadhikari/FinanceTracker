import { makeGetRequest } from "./utils.js";

export default function renderChart(chartName, url) {
    console.log(chartName, url)
    let labelData = [];
    let datasetData = [];

    const fetchDataAndRenderChart = async () => {
        try {
            const data = await makeGetRequest(url);

            if (data) {
                for (let item in data) {
                    labelData.push(item);
                    datasetData.push({
                        label: item,
                        data: [data[item]],
                        borderWidth: 1,
                    });
                }

                const ctx = $("#barChart")[0].getContext("2d"); // Use jQuery to get the canvas context
                new Chart(ctx, {
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
