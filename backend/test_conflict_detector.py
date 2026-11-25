from conflict_detector import detect_conflicts

records = [
    {
        "status": "CONFLICT",
        "issue": "Condition information differs between records",
        "source": "Admission Report and Discharge Report"
    },
    {
        "status": "OK",
        "issue": "No discrepancy recorded",
        "source": "Lab Report"
    }
]

result = detect_conflicts(records)

print("MEDUSA-X CONFLICT DETECTOR TEST")
print("--------------------------------")

for conflict in result:
    print("Issue:", conflict["issue"])
    print("Source:", conflict["source"])
    print("Priority:", conflict["priority"])

if len(result) == 1:
    print("\nTEST PASSED!")
else:
    print("\nTEST FAILED!")