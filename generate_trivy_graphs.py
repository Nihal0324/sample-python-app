import json
import pandas as pd
import matplotlib.pyplot as plt

# Load Trivy JSON output
with open("trivy_output.json") as f:
    data = json.load(f)

# Extract vulnerabilities
vulnerabilities = []
for result in data.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):
        vulnerabilities.append({
            "ID": vuln["VulnerabilityID"],
            "Severity": vuln["Severity"],
            "Package": vuln["PkgName"],
            "Installed Version": vuln["InstalledVersion"]
        })

# Convert to DataFrame
df = pd.DataFrame(vulnerabilities)

# Count vulnerabilities by severity
severity_counts = df["Severity"].value_counts()

# Plot the vulnerability distribution
plt.figure(figsize=(8, 6))
severity_counts.plot(kind="bar", color=["green", "yellow", "orange", "red"])
plt.xlabel("Severity")
plt.ylabel("Count")
plt.title("Vulnerabilities by Severity (Trivy Scan)")
plt.xticks(rotation=45)
plt.grid(axis="y")

# Save the graph
plt.savefig("trivy_vulnerabilities.png")
plt.show()
