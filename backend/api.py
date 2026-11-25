
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from document_processor import extract_text
from timeline import build_timeline
from conflict_detector import detect_conflicts
from medication_checker import check_medications
from safety_dashboard import get_dashboard_summary

app = FastAPI(
    title="MEDUSA-X API",
    description="Clinical Documentation Review Prototype",
    version="1.0"
)

# Frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Homepage API
@app.get("/")
def home():
    return {
        "project": "MEDUSA-X",
        "message": "Backend API is running!"
    }


# Health Check API
@app.get("/health")
def health_check():
    return {
        "status": "running",
        "project": "MEDUSA-X"
    }


# Document Upload API
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith((".pdf", ".txt")):
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
            detail=extracted_text
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in this document."
        )

    return {
        "filename": file.filename,
        "extracted_text": extracted_text,
        "message": "Document text extracted successfully."
    }


# Patient Timeline API
@app.post("/timeline")
def patient_timeline():

    records = [
        {
            "date": "2026-11-23",
            "event": "Lab report received",
            "document": "Lab Report"
        },
        {
            "date": "2026-11-25",
            "event": "Patient admitted",
            "document": "Admission Record"
        },
        {
            "date": "2026-11-24",
            "event": "Prescription record received",
            "document": "Prescription"
        }
    ]

    timeline = build_timeline(records)

    return {
        "patient_timeline": [
            {
                "date": item["date"].strftime("%Y-%m-%d"),
                "event": item["event"],
                "document": item["document"]
            }
            for item in timeline
        ],
        "message": "Patient timeline generated successfully."
    }


# Conflict Detection API
@app.post("/conflicts")
def conflict_detection():

    records = [
        {
            "status": "CONFLICT",
            "issue": "Date mismatch between records",
            "source": "Admission Record and Lab Report"
        },
        {
            "status": "CLEAR",
            "issue": "No conflict found",
            "source": "Prescription Record"
        }
    ]

    conflicts = detect_conflicts(records)

    return {
        "total_conflicts": len(conflicts),
        "conflicts": conflicts,
        "message": "Documentation review findings generated."
    }


# Medication Checker API
@app.post("/medications")
def medication_check():

    records = [
        {
            "medicine": "Medicine A",
            "prescription_status": "DISCONTINUED",
            "discharge_status": "CONTINUED"
        },
        {
            "medicine": "Medicine B",
            "prescription_status": "CONTINUED",
            "discharge_status": "CONTINUED"
        }
    ]

    issues = check_medications(records)

    return {
        "total_issues": len(issues),
        "medication_issues": issues,
        "message": "Medication documentation review completed."
    }


# Safety Dashboard API
@app.get("/dashboard")
def safety_dashboard():

    findings = [
        {
            "issue": "Date mismatch between records",
            "priority": "HIGH"
        },
        {
            "issue": "Medication status mismatch",
            "priority": "HIGH"
        }
    ]

    summary = get_dashboard_summary(
        findings,
        checks_completed=True
    )

    return {
        "dashboard": summary,
        "message": "Dashboard summary generated successfully."
    }
