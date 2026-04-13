AWS Resource Manager & FinOps Dashboard
A modern web application built with Django designed to serve as a central control hub for AWS infrastructure, with a strong focus on financial monitoring and real-time resource management.

📊 Key Features (Finance Module)
The application includes an advanced FinOps dashboard that provides:

Credit Tracking: Automated monitoring of initial AWS credits, current balance, and real-time spending.

Data Visualization (Charts):

Doughnut Chart: Detailed cost distribution by service (EC2, S3, KMS, etc.) for quick consumption analysis.

Line Chart: Daily spending evolution for the current month, enabling easy identification of cost spikes or anomalies.

AWS Cost Explorer Integration: Real-time data fetching using the AWS Cost Explorer API.

Financial Reporting: Built-in functionality to export detailed financial logs to CSV format for auditing and accounting purposes.

🛠️ Tech Stack
Backend: Python 3.11 & Django 5.0.

Cloud SDK: Boto3 (AWS SDK for Python).

Frontend: HTML5, Bootstrap 5 (for a clean, responsive UI).

Data Visualization: Chart.js for interactive and dynamic graphing.

Security: Granular IAM policy implementation following the "Principle of Least Privilege".

🔒 Security & Permissions
The project leverages specific AWS IAM permissions to ensure secure data handling:

ce:GetCostAndUsage for financial data retrieval.

ec2:DescribeInstances for resource monitoring.

s3:ListAllMyBuckets for storage management.

🚀 How It Works
The application queries the AWS Cost Explorer API, processes the raw JSON data, and transforms it into intuitive visual insights. To ensure a seamless user experience, the dashboard includes fallback logic to display sample data when live AWS billing data is still being processed (especially useful for new accounts).