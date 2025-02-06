document.addEventListener("DOMContentLoaded", async function () {
    const recommendationsContainer = document.getElementById("recommendations-container");

    const token = localStorage.getItem("access_token");
    if (!token) {
        recommendationsContainer.innerHTML = `
            <div class="card">
                <p class="error">You must be logged in to see job recommendations.</p>
            </div>`;
        return;
    }

    try {
        const response = await fetch("/cv/recommendations", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch recommendations");
        }

        const data = await response.json();
        recommendationsContainer.innerHTML = data.jobs.map(job => `
            <div class="job-card">
                <div class="job-logo-container">
                    <img src="${job.image || '/static/images/default-company-logo.png'}" 
                         alt="${job.company || 'Company'} Logo" 
                         class="job-logo">
                </div>
                <div class="job-content">
                    <div class="job-header">
                        <div>
                            <h2 class="job-title">${job.title}</h2>
                            <p class="job-company">${job.company || "Unknown Company"}</p>
                        </div>
                        <span class="job-type">${job.type || 'Full-Time'}</span>
                    </div>
                    <div class="skills-list">
                        ${job.skills.map(skill =>
            `<span class="skill-tag">${skill}</span>`
        ).join('')}
                    </div>
                     <a href="${job.link}" class="apply-button" target="_blank">Apply Now</a>
                </div>
            </div>
        `).join("");

    } catch (error) {
        recommendationsContainer.innerHTML = `
            <div class="card">
                <p class="error">Error loading recommendations: ${error.message}</p>
            </div>`;
    }
});