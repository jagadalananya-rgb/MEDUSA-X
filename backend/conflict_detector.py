def detect_conflicts(records):

    conflicts = []

    for record in records:

        if record["status"] == "CONFLICT":
            conflicts.append({
                "issue": record["issue"],
                "source": record["source"],
                "priority": "HIGH"
            })

    return conflicts