from timeline import build_timeline

records = [
    {
        "date": "2026-11-27",
        "event": "Discharge",
        "document": "Discharge Report"
    },
    {
        "date": "2026-11-25",
        "event": "Admission",
        "document": "Admission Report"
    },
    {
        "date": "2026-11-26",
        "event": "Prescription",
        "document": "Prescription Report"
    }
]

result = build_timeline(records)

print("MEDUSA-X TIMELINE TEST")
print("----------------------")

for item in result:
    print(item["date"].strftime("%d-%m-%Y"), "-", item["event"])

if result and result[0]["event"] == "Admission":
    print("\nTEST PASSED!")
else:
    print("\nTEST FAILED!")