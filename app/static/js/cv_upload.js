document.addEventListener("DOMContentLoaded", function () {
    const uploadButton = document.getElementById("upload-cv-btn");
    const fileInput = document.getElementById("cv-file-input");
    const uploadProgressContainer = document.getElementById("upload-progress-container");
    const uploadProgressBar = document.getElementById("upload-progress");
    const uploadProgressText = document.getElementById("upload-progress-text");
    const statusMessage = document.getElementById("status-message");

    // Reset UI state
    const resetUI = () => {
        uploadProgressContainer.style.display = "none";
        uploadProgressBar.style.width = "0%";
        uploadProgressText.innerText = "";
        statusMessage.innerHTML = "";
    };

    uploadButton.addEventListener("click", () => {
        fileInput.click();
    });

    fileInput.addEventListener("change", async function (event) {
        const file = event.target.files[0];
        if (!file) return;

        // Reset UI state before starting new upload
        resetUI();

        document.getElementById("file-name").innerText = file.name;
        uploadProgressContainer.style.display = "block";
        uploadProgressBar.style.width = "0%";
        uploadProgressText.innerText = "Uploading...";

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/cv/upload", {
                method: "POST",
                body: formData,
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("access_token")}`
                }
            });

            const data = await response.json();

            if (!response.ok) {
                // In case of error, hide the progress container and show error message
                uploadProgressContainer.style.display = "none";
                statusMessage.innerHTML = `<p class="error">${data.message || "Something went wrong!"}</p>`;
                return;
            }

            // Clear any previous error messages on success
            statusMessage.innerHTML = "";
            uploadProgressBar.style.width = "100%";
            uploadProgressText.innerText = "Upload complete! Checking job recommendations...";

            setTimeout(() => {
                window.location.href = "/job_recommendations.html";
            }, 2000);

        } catch (error) {
            // In case of unexpected error, reset UI and show error message
            uploadProgressContainer.style.display = "none";
            statusMessage.innerHTML = `<p class="error">An unexpected error occurred.</p>`;
        }
    });
});