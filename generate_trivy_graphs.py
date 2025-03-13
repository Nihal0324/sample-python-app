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
            "Installed Version": vuln["InstalledVersion"],
            "Description": vuln.get("Description", "No description")
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
plt.title("Trivy Vulnerabilities by Severity")
plt.xticks(rotation=45)
plt.grid(axis="y")

# Save the graph
graph_path = "trivy_vulnerabilities.png"
plt.savefig(graph_path)
plt.close()

# Create HTML report with vulnerabilities + graph
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Trivy Vulnerability Report</title>
    <style>
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid black; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Trivy Vulnerability Report</h1>
    <img src="{graph_path}" alt="Trivy Vulnerability Graph" width="600">
    <h2>Vulnerability Details</h2>
    <table>
        <tr>
            <th>Vulnerability ID</th>
            <th>Severity</th>
            <th>Package</th>
            <th>Installed Version</th>
            <th>Description</th>
        </tr>
"""

# Add vulnerabilities to the HTML table
for _, row in df.iterrows():
    html_content += f"""
        <tr>
            <td>{row["ID"]}</td>
            <td>{row["Severity"]}</td>
            <td>{row["Package"]}</td>
            <td>{row["Installed Version"]}</td>
            <td>{row["Description"]}</td>
        </tr>
    """

html_content += """
    </table>
</body>
</html>
"""

# Save HTML report
with open("trivy_graph_report.html", "w") as f:
    f.write(html_content)

print("✅ Trivy HTML report generated successfully!")
