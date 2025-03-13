import sys
import json
import matplotlib.pyplot as plt

# Read JSON file path from arguments
if len(sys.argv) < 2:
    print("Usage: python3 generate_trivy_graphs.py <json_file_path>")
    sys.exit(1)

json_file = sys.argv[1]

# Load JSON report
with open(json_file) as f:
    data = json.load(f)

# Extract vulnerability data
severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
for vuln in data.get("Results", []):
    for vulnerability in vuln.get("Vulnerabilities", []):
        severity = vulnerability.get("Severity", "UNKNOWN")
        if severity in severity_counts:
            severity_counts[severity] += 1

# Plot Graph
plt.bar(severity_counts.keys(), severity_counts.values(), color=["blue", "yellow", "orange", "red"])
plt.xlabel("Severity")
plt.ylabel("Count")
plt.title("Trivy Vulnerabilities by Severity")
plt.savefig("trivy_graph.png")

print("✅ Trivy graph generated successfully!")

