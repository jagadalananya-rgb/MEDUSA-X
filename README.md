# MEDUSA-X
### Agentic Clinical Intelligence for Patient Record Review

## Problem Statement
Patient information is often spread across admission notes, laboratory reports, prescriptions, and discharge summaries. This makes it difficult to identify missing information and documentation inconsistencies.

## Our Solution
MEDUSA-X is a clinical documentation review prototype that organizes patient records and flags potential inconsistencies for professional review.

It does not guess or make independent medical decisions.

## Key Features
1. **Patient Timeline** – Organizes patient records chronologically.
2. **Documentation Conflict Review** – Flags explicitly identified documentation conflicts.
3. **Medication Review** – Detects medication status mismatches in demo records.
4. **Safety Review Dashboard** – Displays the priority of detected issues.

## Technology Stack
- Python
- FastAPI
- HTML
- CSS
- JavaScript
- Rule-based checking

## How to Run

Install dependencies:

    pip install -r requirements.txt

Start the backend:

    python -m uvicorn api:app --reload --app-dir backend

Open API documentation:

    http://127.0.0.1:8000/docs

Open frontend using VS Code Live Server:
    frontend/index.html

## Project Status
Hackathon prototype.

## Safety Note
MEDUSA-X is not a diagnostic system or a replacement for healthcare professionals. All demonstrations use fictional data. Findings require qualified professional review.
