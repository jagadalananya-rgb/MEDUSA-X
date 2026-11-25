from medication_checker import check_medications

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

result = check_medications(records)

print("MEDUSA-X MEDICATION CHECKER TEST")
print("--------------------------------")

for issue in result:
    print("Medicine:", issue["medicine"])
    print("Issue:", issue["issue"])
    print("Priority:", issue["priority"])
    print("Message:", issue["message"])

if len(result) == 1:
    print("\nTEST PASSED!")
else:
    print("\nTEST FAILED!")