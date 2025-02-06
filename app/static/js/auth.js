document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');

    if (!token) {
        // Redirect to the login page if no token is found
        window.location.href = '/';
        return;
    }

    // Fetch the CV upload page with the token in the headers
    fetch("http://localhost:8000/cv-upload", {
        headers: {
            "Authorization": `Bearer ${token}`,
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.text(); // or response.json() if the response is JSON
    })
    .then(data => {
        console.log("CV upload page loaded successfully");
        // Render the CV upload page or handle the response
    })
    .catch(error => {
        console.error("Error loading CV upload page:", error);
        alert("Failed to load CV upload page. Please try again.");
    });
});