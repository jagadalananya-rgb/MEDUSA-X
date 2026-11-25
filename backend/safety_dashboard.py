def get_review_status(findings, checks_completed=True):

    if not checks_completed:
        return "YELLOW"

    for finding in findings:
        if finding.get("priority") == "HIGH":
            return "RED"

    if findings:
        return "YELLOW"

    return "GREEN"


def get_dashboard_summary(findings, checks_completed=True):

    return {
        "status": get_review_status(
            findings, checks_completed
        ),
        "total_issues": len(findings),
        "high_priority": sum(
            1 for item in findings
            if item.get("priority") == "HIGH"
        ),
        "checks_completed": checks_completed
    }