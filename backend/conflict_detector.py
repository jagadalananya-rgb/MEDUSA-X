def detect_conflicts(records):

    conflicts = []

    for record in records:

        if record.get("status") == "CONFLICT":

            conflicts.append({
                "issue": record.get("issue", "Unknown issue"),
                "source": record.get("source", "Unknown source"),
                "priority": record.get("priority", "HIGH")
            })

    return conflicts