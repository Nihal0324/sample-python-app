import json
import pandas as pd

# Load Trivy JSON output
with open("trivy_output.json") as f:
    data = json.load(f)

# Extract vulnerabilities
vulnerabilities = []
for result in data.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):
        vulnerabilities.append({
            "Severity": vuln["Severity"]
        })

# Convert to DataFrame
df = pd.DataFrame(vulnerabilities)

# Count vulnerabilities by severity
severity_counts = df["Severity"].value_counts().sort_index()

# Save as CSV for Jenkins Plot Plugin
csv_path = "trivy_vulnerability_data.csv"
severity_counts.to_csv(csv_path, header=["Count"])

print(f"✅ Trivy graph data saved: {csv_path}")
