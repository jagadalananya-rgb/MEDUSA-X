
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from document_processor import extract_text
from timeline import build_timeline
from conflict_detector import detect_conflicts
from medication_checker import check_medications
from safety_dashboard import get_dashboard_summary
from llm_analyzer import analyze_document


app = FastAPI(
    title="MEDUSA-X API",
    description="Clinical Documentation Review Prototype",
    version="1.3"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Stores the latest uploaded documents
current_document_text = None
current_filenames = []


# Remove exact duplicate records
def remove_duplicates(records, keys):

    unique_records = []
    seen = set()

    for record in records:

        record_key = tuple(
            str(record.get(key, "")).strip().lower()
            for key in keys
        )

        if record_key not in seen:
            seen.add(record_key)
            unique_records.append(record)

    return unique_records


# Read labelled information from uploaded documents
def parse_document(text):

    lines = text.splitlines()

    timeline_records = []
    medication_records = []
    conflict_records = []

    timeline_record = {}
    medication_record = {}
    conflict_record = {}

    for line in lines:

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().upper()
        value = value.strip()

        if not value:
            continue

        # Timeline information
        if key == "DATE":

            if timeline_record:
                timeline_records.append(timeline_record)

            timeline_record = {"date": value}

        elif key == "EVENT":
            timeline_record["event"] = value

        elif key == "DOCUMENT":
            timeline_record["document"] = value

        # Medication information
        elif key == "MEDICINE":

            if medication_record:
                medication_records.append(medication_record)

            medication_record = {"medicine": value}

        elif key == "PRESCRIPTION_STATUS":
            medication_record["prescription_status"] = value.upper()

        elif key == "DISCHARGE_STATUS":
            medication_record["discharge_status"] = value.upper()

        # Documentation conflict information
        elif key == "CONFLICT":

            if conflict_record:
                conflict_records.append(conflict_record)

            conflict_record = {
                "status": "CONFLICT",
                "issue": value
            }

        elif key == "SOURCE" and conflict_record:
            conflict_record["source"] = value

    # Save final records
    if timeline_record:
        timeline_records.append(timeline_record)

    if medication_record:
        medication_records.append(medication_record)

    if conflict_record:
        conflict_records.append(conflict_record)

    # Keep complete timeline records
    timeline_records = [
        record for record in timeline_records
        if all(key in record for key in (
            "date", "event", "document"
        ))
    ]

    # Remove exact duplicate timeline entries
    timeline_records = remove_duplicates(
        timeline_records,
        ["date", "event", "document"]
    )

    # Combine medication information for the same medicine
    merged_medications = {}

    for record in medication_records:

        medicine = record["medicine"].strip().lower()

        if medicine not in merged_medications:
            merged_medications[medicine] = {
                "medicine": record["medicine"]
            }

        merged_medications[medicine].update({
            key: value
            for key, value in record.items()
            if key != "medicine"
        })

    medication_records = [
        record for record in merged_medications.values()
        if all(key in record for key in (
            "medicine",
            "prescription_status",
            "discharge_status"
        ))
    ]

    # Keep complete conflict records
    conflict_records = [
        record for record in conflict_records
        if "source" in record and "issue" in record
    ]

    # Remove exact duplicate conflict entries
    conflict_records = remove_duplicates(
        conflict_records,
        ["issue", "source"]
    )

    return timeline_records, conflict_records, medication_records


def get_uploaded_records():

    if current_document_text is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload documents first."
        )

    return parse_document(current_document_text)


@app.get("/")
def home():

    return {
        "project": "MEDUSA-X",
        "message": "Backend API is running!"
    }


@app.get("/health")
def health_check():

    return {
        "status": "running",
        "project": "MEDUSA-X"
    }


# Upload multiple PDF and TXT documents
@app.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):

    global current_document_text, current_filenames

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Please select at least one document."
        )

    extracted_documents = []
    uploaded_filenames = []

    for file in files:

        if not file.filename or not file.filename.lower().endswith(
            (".pdf", ".txt")
        ):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and TXT files are supported."
            )

        content = await file.read()

        class UploadedFile:

            def __init__(self, name, data):
                self.name = name
                self.data = data

            def getvalue(self):
                return self.data

        uploaded_file = UploadedFile(file.filename, content)

        extracted_text = extract_text(uploaded_file)

        if extracted_text.startswith("Document reading error:"):
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename}: {extracted_text}"
            )

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail=f"No readable text found in {file.filename}."
            )

        extracted_documents.append(
            f"\nDOCUMENT_FILE: {file.filename}\n{extracted_text}"
        )

        uploaded_filenames.append(file.filename)

    # Store uploaded documents
    current_document_text = "\n".join(extracted_documents)
    current_filenames = uploaded_filenames

    return {
        "filenames": current_filenames,
        "total_documents": len(current_filenames),
        "extracted_text": current_document_text,
        "message": "Multiple documents uploaded successfully."
    }


# Patient Timeline
@app.post("/timeline")
def patient_timeline():

    timeline_records, _, _ = get_uploaded_records()

    timeline = build_timeline(timeline_records)

    return {
        "patient_timeline": [
            {
                "date": item["date"].strftime("%Y-%m-%d"),
                "event": item["event"],
                "document": item["document"]
            }
            for item in timeline
        ],
        "message": "Timeline generated successfully."
    }


# Documentation Conflict Detection
@app.post("/conflicts")
def conflict_detection():

    _, conflict_records, _ = get_uploaded_records()

    conflicts = detect_conflicts(conflict_records)

    return {
        "total_conflicts": len(conflicts),
        "conflicts": conflicts,
        "message": "Conflict review generated successfully."
    }


# Medication Review
@app.post("/medications")
def medication_check():

    _, _, medication_records = get_uploaded_records()

    issues = check_medications(medication_records)

    # Remove exact duplicate medication findings
    issues = remove_duplicates(
        issues,
        ["medicine", "issue", "priority", "message"]
    )

    return {
        "total_issues": len(issues),
        "medication_issues": issues,
        "message": "Medication review generated successfully."
    }


# Safety Review Dashboard
@app.get("/dashboard")
def safety_dashboard():

    _, conflict_records, medication_records = get_uploaded_records()

    conflicts = detect_conflicts(conflict_records)

    medication_issues = check_medications(medication_records)

    medication_issues = remove_duplicates(
        medication_issues,
        ["medicine", "issue", "priority", "message"]
    )

    findings = []

    for conflict in conflicts:

        findings.append({
            "issue": conflict["issue"],
            "priority": conflict["priority"]
        })

    for issue in medication_issues:

        findings.append({
            "issue": issue["issue"],
            "priority": issue["priority"]
        })

    # Remove exact duplicate dashboard findings
    findings = remove_duplicates(
        findings,
        ["issue", "priority"]
    )

    summary = get_dashboard_summary(
        findings,
        checks_completed=True
    )

    return {
        "dashboard": summary,
        "message": "Dashboard generated successfully."
    }


# Optional LLM Documentation Review
@app.post("/llm-review")
def llm_review():

    if current_document_text is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload documents first."
        )

    result = analyze_document(current_document_text)

    return {
        "llm_review": result,
        "message": "Optional documentation review completed."
    }
