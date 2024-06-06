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

emailField = $("#emailField");
emailFeedback = $("#emailFeedback");

emailField.on("keyup", (e) => {
    const emailVal = e.target.value;
    if (emailVal.length > 8) {
        fetch("/auth/email-validation", {
            method: "POST",
            body: JSON.stringify({
                email: emailVal,
            }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.email_error) {
                    emailField.addClass("is-invalid");
                    emailFeedback.css("display", "block");
                    emailFeedback.find("p").text(data.email_error);
                } else {
                    emailField.removeClass("is-invalid");
                    emailFeedback.css("display", "none");
                    // emailFeedback.find("p").text(data.email_error);
                }
            });
    }
});
