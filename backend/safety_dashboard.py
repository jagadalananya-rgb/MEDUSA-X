
def get_dashboard_summary(findings, checks_completed=True):

    total_issues = len(findings)

    high_priority = sum(
        1 for item in findings
        if item.get("priority") == "HIGH"
    )

    if high_priority > 0:
        status = "RED"

    elif total_issues > 0:
        status = "YELLOW"

    elif checks_completed:
        status = "GREEN"

    else:
        status = "PENDING"

    return {
        "status": status,
        "total_issues": total_issues,
        "high_priority": high_priority,
        "checks_completed": checks_completed
    }
