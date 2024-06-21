const ctx = document.getElementById("myChart");

labelData = [];
datasetData = [];

fetch("/expense-category-data", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
})
    .then((res) => res.json())
    .then((data) => {
        for (item in data) {
            console.log(item);
            labelData.push(item);
            datasetData.push({
                label: item,
                data: [data[item]],
                borderWidth: 1,
            });
        }

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
    });
