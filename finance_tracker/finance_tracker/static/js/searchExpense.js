$(document).ready(function () {
    searchField = $("#searchField");

    originalTable = $(".original-table");
    ajaxTable = $(".ajax-table");

    ajaxTable.hide();

    searchField.on("keyup", (e) => {
        const searchVal = e.target.value;

        if (searchVal.trim().length > 0) {
            originalTable.hide();
            fetch("/search-expenses", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    searchText: searchVal,
                }),
            })
                .then((res) => {
                    if (!res.ok) {
                        throw new Error(
                            "Network response was not ok " + res.statusText
                        );
                    }
                    return res.json();
                })
                .then((data) => {
                    ajaxTable.show();
                    const tbody = $(".ajax-table").find("tbody");
                    tbody.empty(); // Clear previous results

                    if (data.length < 1) {
                        tbody.append(
                            "<tr><td colspan='5'>No data found</td></tr>"
                        );
                    } else {
                        data.forEach((item) => {
                            tbody.append(`
                            <tr>
                                <td>${item.category_name}</td>
                                <td>${item.description}</td>
                                <td>${item.date}</td>
                                <td>${item.amount}</td>
                                <td>sdfd</td>
                            </tr>
                        `);
                        });
                    }
                })
                .catch((error) => {
                    console.error(
                        "There has been a problem with your fetch operation:",
                        error
                    );
                });
        } else if (searchVal == "") {
            // If the search field is empty, show the original table and hide the AJAX table
            ajaxTable.hide();
            originalTable.show();
        }
    });
});
