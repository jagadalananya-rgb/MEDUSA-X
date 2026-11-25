
const API_URL = "http://127.0.0.1:8000";

// Upload Document
const uploadButton = document.getElementById("uploadButton");

uploadButton.addEventListener("click", async function () {

    const fileInput = document.getElementById("fileInput");
    const result = document.getElementById("result");
    const file = fileInput.files[0];

    if (!file) {
        result.textContent = "Please select a document first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    result.textContent = "Uploading document...";

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Upload failed.");
        }

        result.textContent =
            "Filename: " + data.filename +
            "\n\nExtracted Text:\n" + data.extracted_text +
            "\n\n" + data.message;

    } catch (error) {
        result.textContent = "Error: " + error.message;
    }
});


// Patient Timeline
document.getElementById("timelineButton")
.addEventListener("click", async function () {

    const output = document.getElementById("timelineResult");
    output.textContent = "Loading timeline...";

    try {
        const response = await fetch(`${API_URL}/timeline`, {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Timeline request failed.");
        }

        output.textContent = data.patient_timeline.map(item =>
            `${item.date} - ${item.event} (${item.document})`
        ).join("\n");

    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
});


// Documentation Conflicts
document.getElementById("conflictButton")
.addEventListener("click", async function () {

    const output = document.getElementById("conflictResult");
    output.textContent = "Checking documentation...";

    try {
        const response = await fetch(`${API_URL}/conflicts`, {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Conflict check failed.");
        }

        if (data.conflicts.length === 0) {
            output.textContent = "No configured conflicts found.";
        } else {
            output.textContent = data.conflicts.map(item =>
                `Issue: ${item.issue}\nSource: ${item.source}\nPriority: ${item.priority}`
            ).join("\n\n");
        }

    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
});


// Medication Review
document.getElementById("medicationButton")
.addEventListener("click", async function () {

    const output = document.getElementById("medicationResult");
    output.textContent = "Reviewing medication records...";

    try {
        const response = await fetch(`${API_URL}/medications`, {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Medication review failed.");
        }

        if (data.medication_issues.length === 0) {
            output.textContent = "No configured medication mismatches found.";
        } else {
            output.textContent = data.medication_issues.map(item =>
                `Medicine: ${item.medicine}\nIssue: ${item.issue}\nPriority: ${item.priority}\nMessage: ${item.message}`
            ).join("\n\n");
        }

    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
});


// Safety Dashboard
document.getElementById("dashboardButton")
.addEventListener("click", async function () {

    const output = document.getElementById("dashboardResult");
    output.textContent = "Loading dashboard...";

    try {
        const response = await fetch(`${API_URL}/dashboard`);

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Dashboard request failed.");
        }

        const dashboard = data.dashboard;

        output.textContent =
            `Review Status: ${dashboard.status}\n` +
            `Total Issues: ${dashboard.total_issues}\n` +
            `High Priority: ${dashboard.high_priority}\n` +
            `Checks Completed: ${dashboard.checks_completed ? "Yes" : "No"}`;

    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
});
