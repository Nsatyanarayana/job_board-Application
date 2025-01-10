document.getElementById("register-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;
    const API_BASE_URL = "http://127.0.0.1:8800";

    const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password, role }),
    });

    const result =  response.json();
    console.log(result)
    if (response.ok) {
        alert(result.message);
        window.location.href = "login.html";  
    } else {
        alert(result.detail);
    }
});

document.getElementById("login-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const API_BASE_URL = "http://127.0.0.1:8800";

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });  

    const result = await response.json();
    // keep user details in session storage or local storage
    console.log(result)
    if (response.ok) {
        const role = result.role
        const casingRole = role.toLowerCase();
        console.log(casingRole)

        if (role == "employer") {
            window.location.href = "employer/dashboard.html";
        } else {
            window.location.href = "job-seeker/dashboard.html";
        }
    } else {
        alert(result.detail);
    }
});
