
const API_URL = "http://127.0.0.1:8000";

const fileInput = document.querySelector("#medicalFiles");
const fileStatus = document.querySelector("#fileStatus");
const uploadButton = document.querySelector("#uploadBtn");

const timelineResults = document.querySelector("#timelineResults");
const conflictResults = document.querySelector("#conflictResults");
const medicationResults = document.querySelector("#medicationResults");
const dashboardResults = document.querySelector("#dashboardResults");


// Display message
function showMessage(element, message) {
    element.textContent = message;
}


// Load Patient Timeline
async function loadTimeline() {

    const response = await fetch(API_URL + "/timeline", {
        method: "POST"
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Timeline loading failed");
    }

    timelineResults.innerHTML = "";

    if (data.patient_timeline.length === 0) {
        showMessage(timelineResults, "No timeline records found.");
        return;
    }

    data.patient_timeline.forEach(item => {

        const card = document.createElement("div");
        card.className = "timeline-item";

        const date = document.createElement("span");
        date.className = "timeline-date";
        date.textContent = item.date;

        const heading = document.createElement("h3");
        heading.textContent = item.event;

        const documentName = document.createElement("small");
        documentName.textContent = "Source: " + item.document;

        card.append(date, heading, documentName);
        timelineResults.appendChild(card);
    });
}


// Load Documentation Conflicts
async function loadConflicts() {

    const response = await fetch(API_URL + "/conflicts", {
        method: "POST"
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Conflict review failed");
    }

    conflictResults.innerHTML = "";

    if (data.conflicts.length === 0) {
        showMessage(
            conflictResults,
            "No labelled documentation conflicts found."
        );
        return;
    }

    data.conflicts.forEach(item => {

        const card = document.createElement("div");
        card.className = "conflict-item";

        const status = document.createElement("span");
        status.className = "conflict-status";
        status.textContent = "Documentation Mismatch";

        const heading = document.createElement("h3");
        heading.textContent = item.issue;

        const source = document.createElement("small");
        source.textContent = "Source: " + item.source;

        const priority = document.createElement("p");
        priority.textContent = "Priority: " + item.priority;

        const review = document.createElement("p");
        review.className = "review-label";
        review.textContent = "Requires professional review.";

        card.append(status, heading, source, priority, review);
        conflictResults.appendChild(card);
    });
}


// Load Medication Review
async function loadMedications() {

    const response = await fetch(API_URL + "/medications", {
        method: "POST"
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Medication review failed");
    }

    medicationResults.innerHTML = "";

    if (data.medication_issues.length === 0) {
        showMessage(
            medicationResults,
            "No medication documentation mismatches found."
        );
        return;
    }

    data.medication_issues.forEach(item => {

        const card = document.createElement("div");
        card.className = "medication-item";

        const status = document.createElement("span");
        status.className = "medication-status";
        status.textContent = item.priority + " PRIORITY";

        const heading = document.createElement("h3");
        heading.textContent = item.medicine;

        const issue = document.createElement("p");
        issue.textContent = item.issue;

        const message = document.createElement("p");
        message.textContent = item.message;

        const review = document.createElement("p");
        review.className = "medication-warning";
        review.textContent = "Requires professional review.";

        card.append(status, heading, issue, message, review);
        medicationResults.appendChild(card);
    });
}


// Load Safety Review Dashboard
async function loadDashboard() {

    const response = await fetch(API_URL + "/dashboard");

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Dashboard loading failed");
    }

    const summary = data.dashboard;

    dashboardResults.innerHTML = "";

    const status = document.createElement("span");
    status.className = "dashboard-status";

    status.textContent = "STATUS: " + summary.status;

    if (summary.status === "RED") {
        status.classList.add("status-red");
    } else if (summary.status === "YELLOW") {
        status.classList.add("status-yellow");
    } else if (summary.status === "GREEN") {
        status.classList.add("status-green");
    } else {
        status.classList.add("status-pending");
    }

    const total = document.createElement("p");
    total.textContent = "Total findings: " + summary.total_issues;

    const high = document.createElement("p");
    high.textContent = "High-priority findings: " + summary.high_priority;

    const completed = document.createElement("p");
    completed.textContent =
        "Software checks completed: " +
        (summary.checks_completed ? "Yes" : "No");

    const note = document.createElement("p");
    note.textContent =
        "This status summarizes configured documentation checks only. Professional review is required.";

    dashboardResults.append(status, total, high, completed, note);
}


// Show selected files
fileInput.addEventListener("change", function () {

    const files = Array.from(fileInput.files);

    if (files.length === 0) {
        fileStatus.textContent = "No files selected";
        return;
    }

    fileStatus.textContent =
        files.length + " document(s) selected: " +
        files.map(file => file.name).join(", ");
});


// Upload multiple documents and run all reviews
uploadButton.addEventListener("click", async function () {

    const files = Array.from(fileInput.files);

    if (files.length === 0) {
        alert("Please select PDF or TXT documents first.");
        return;
    }

    const formData = new FormData();

    files.forEach(file => {
        formData.append("files", file);
    });

    uploadButton.disabled = true;
    uploadButton.textContent = "Uploading...";

    fileStatus.textContent = "Uploading documents...";

    try {

        const response = await fetch(API_URL + "/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Upload failed");
        }

        fileStatus.textContent =
            "Successfully uploaded " +
            data.total_documents +
            " document(s): " +
            data.filenames.join(", ");

        // Run all review modules
        await loadTimeline();
        await loadConflicts();
        await loadMedications();
        await loadDashboard();

        alert("Upload and documentation review completed!");

    } catch (error) {

        fileStatus.textContent = "Error: " + error.message;

        alert("Error: " + error.message);

    } finally {

        uploadButton.disabled = false;
        uploadButton.textContent = "Upload Documents";
    }
});
