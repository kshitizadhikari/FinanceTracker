import { makeGetRequest } from "./utils.js";

let labelData = [];
let datasetData = [];

const renderChart = async () => {
    const url = "/expense-category-data";
    const data = await makeGetRequest(url);

    if (data) {
        for (let item in data) {
            console.log(item);
            labelData.push(item);
            datasetData.push({
                label: item,
                data: [data[item]],
                borderWidth: 1,
            });
        }

        const ctx = document.getElementById("myChart").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["expenses"],
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
};

document.addEventListener("DOMContentLoaded", renderChart);
