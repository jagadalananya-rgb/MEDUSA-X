def check_medications(records):

    issues = []

    for record in records:

        if (
            record["prescription_status"] == "DISCONTINUED"
            and record["discharge_status"] == "CONTINUED"
        ):

            issues.append({
                "medicine": record["medicine"],
                "issue": "Medication status mismatch",
                "priority": "HIGH",
                "message": (
                    "Prescription says discontinued, "
                    "but discharge record says continued."
                )
            })

    return issues