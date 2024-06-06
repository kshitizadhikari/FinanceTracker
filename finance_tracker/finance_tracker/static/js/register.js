console.log("hello from register.js");

usernameField = $("#usernameField");
invalidFeedback = $("#invalidFeedback");

usernameField.on("keyup", (e) => {
    const usernameVal = e.target.value;
    if (usernameVal.length > 2) {
        fetch("/auth/username-validation", {
            method: "POST",
            body: JSON.stringify({
                username: usernameVal,
            }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.username_error) {
                    usernameField.addClass("is-invalid");
                    invalidFeedback.css("display", "block");
                    invalidFeedback.find("p").text(data.username_error);
                } else {
                    usernameField.removeClass("is-invalid");
                    invalidFeedback.css("display", "none");
                    // invalidFeedback.find("p").text(data.username_error);
                }
            });
    }
});
