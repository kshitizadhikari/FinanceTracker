$(document).ready(function () {
    const submitBtn = $("#submitBtn");

    // User
    const usernameField = $("#usernameField");
    const usernameCheck = $(".usernameCheck");
    const invalidFeedback = $("#invalidFeedback");
    usernameCheck.hide();
    usernameField.on("keyup", (e) => {
        const usernameVal = e.target.value;
        if (usernameVal.length > 2) {
            usernameCheck.text(`Checking ${usernameVal}`).show();
            invalidFeedback.hide();

            fetch("/auth/username-validation", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: usernameVal }),
            })
                .then((res) => res.json())
                .then((data) => {
                    usernameCheck.hide();
                    if (data.username_error) {
                        // submitBtn.attr("disabled", "disabled");
                        submitBtn.prop("disabled", true);
                        usernameField.addClass("is-invalid");
                        invalidFeedback.find("p").text(data.username_error);
                        invalidFeedback.show();
                    } else {
                        submitBtn.prop("disabled", false);
                        usernameField.removeClass("is-invalid");
                        invalidFeedback.hide();
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    usernameCheck.hide();
                    invalidFeedback
                        .find("p")
                        .text("An error occurred while checking the username.");
                    invalidFeedback.show();
                });
        } else {
            usernameField.removeClass("is-invalid");
            invalidFeedback.hide();
            usernameCheck.hide();
        }
    });

    // Email
    const emailField = $("#emailField");
    const emailCheck = $(".emailCheck");
    const emailFeedback = $("#emailFeedback");
    emailCheck.hide();
    emailField.on("keyup", (e) => {
        const emailVal = e.target.value;
        if (emailVal.length > 6) {
            emailCheck.text(`Checking ${emailVal}`).show();
            emailFeedback.hide();

            fetch("/auth/email-validation", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email: emailVal }),
            })
                .then((res) => res.json())
                .then((data) => {
                    emailCheck.hide();
                    if (data.email_error) {
                        emailField.addClass("is-invalid");
                        submitBtn.prop("disabled", true);
                        emailFeedback.find("p").text(data.email_error);
                        emailFeedback.show();
                    } else {
                        submitBtn.prop("disabled", false);
                        emailField.removeClass("is-invalid");
                        emailFeedback.hide();
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                    emailCheck.hide();
                    emailFeedback
                        .find("p")
                        .text("An error occurred while checking the username.");
                    emailFeedback.show();
                });
        } else {
            emailField.removeClass("is-invalid");
            emailFeedback.hide();
            emailCheck.hide();
        }
    });

    // Password
    const showPassword = $(".showPassword");
    const passwordField = $("#passwordField");

    handlePasswordToggle = (e) => {
        if (passwordField.attr("type") === "password") {
            passwordField.attr("type", "text");
            showPassword.text("HIDE");
        } else {
            passwordField.attr("type", "password");
            showPassword.text("SHOW");
        }
    };
    showPassword.on("click", handlePasswordToggle);

    showPassword.hover(
        function () {
            $(this).css("cursor", "pointer");
        },
        function () {
            $(this).css("cursor", "default");
        }
    );
    
    // Register Form Submit

    handleSubmit = (e) => {
        console.log(e.data);
    };
    submitBtn.on("click", handleSubmit);
});
