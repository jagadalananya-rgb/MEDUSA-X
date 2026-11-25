from safety_dashboard import get_dashboard_summary

print("MEDUSA-X SAFETY DASHBOARD TEST")
print("--------------------------------")

# Test 1: High-priority issue
findings = [
    {"priority": "HIGH"}
]

result = get_dashboard_summary(findings)
print("Test 1:", result["status"])

# Test 2: Low-priority issue
findings = [
    {"priority": "LOW"}
]

result = get_dashboard_summary(findings)
print("Test 2:", result["status"])

# Test 3: No issues
findings = []

result = get_dashboard_summary(findings)
print("Test 3:", result["status"])

# Test 4: Checks not completed
result = get_dashboard_summary([], checks_completed=False)
print("Test 4:", result["status"])

print("\nTESTS COMPLETED!")