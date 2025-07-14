# 📦 Release Management Documentation Agent (GitHub & Jira)

This Python-based automation agent streamlines the creation of release documentation by integrating data from GitHub and Jira. It extracts release notes for a given version tag, identifies related Jira tickets, enriches them with metadata, generates a formatted Word document, and creates a new Jira ticket with the compiled release information using Atlassian Document Format (ADF).

---

## 🚀 Project Goal

As part of the 2025 Internship Project, this agent was developed to automate and centralize release documentation into a Jira ticket with minimal human effort.

---

## ⚙️ Functionality Overview

- 🔢 Accepts a version tag as input (e.g., `v1.108.1`)
- 🐙 Retrieves release notes from GitHub via API
- 🔗 Extracts and queries Jira ticket IDs like `CWB-XXXX`
- 📄 Generates a Word document summarizing the release
- 🧾 Creates a Jira ticket using ADF with summary and details

---

## 📥 Prerequisites

- Python 3.10+
- GitHub personal access token
- Jira API token
- Access to the GitHub and Jira project

---

## 🧪 Installation

```bash
git clone https://github.com/your-org/release-agent.git
cd release-agent
pip install -r requirements.txt
Required libraries: python-docx, python-dotenv, requests, PyGithub

🔐 Environment Configuration
Create a .env file in the root folder with the following:

env
Copy
Edit
GITHUB_TOKEN=ghp_yourgithubtoken
GITHUB_REPO=yourorg/yourrepo

JIRA_EMAIL=your_email@example.com
JIRA_TOKEN=your_jira_api_token
JIRA_URL=https://yourdomain.atlassian.net
JIRA_PROJECT_KEY=CWB
JIRA_ISSUE_TYPE=Task
Tip: Never commit your real .env file — use .env.example for sharing.

▶️ How to Run the Agent
bash
Copy
Edit
python main.py
Then input a release version tag when prompted:

less
Copy
Edit
🔢 Escribe el tag de versión (ej: v1.109.0-beta.4):
Example:

Copy
Edit
v1.108.1
The script will:

Retrieve release notes from GitHub

Extract Jira ticket IDs

Query ticket summaries and statuses

Generate a .docx release document

Create a Jira ticket with the full release info

📂 Output Example
📝 Word Document (release_v1.108.1.docx)
pgsql
Copy
Edit
Release Management Document - v1.108.1

Summary of Changes
• webapp: [CWB-14290] internal calls to identity from app router

Detailed Release Notes
1. webapp: [CWB-14290] internal calls to identity from app router
🧾 Jira Ticket (auto-created)
Summary:
Release Management Document - v1.108.1

Description:

pgsql
Copy
Edit
📦 Release Version: v1.108.1  
📅 Release Date: 2025-06-10

🔹 Summary of Changes  
- CWB-14290: [WEB] Use internal identity end-point instead external for web server request

📋 Detailed Release Notes  
CWB-14290 – [WEB] Use internal identity end-point instead external for web server request  
(Status: Done) – https://televisaunivision.atlassian.net/browse/CWB-14290
🧠 Known Limitations
Only works with release notes that mention Jira tickets (CWB-1234)

Only supports public or authorized GitHub repositories

One version input per execution

✅ Success Criteria
Successfully pulls GitHub release notes

Accurately enriches Jira ticket details

Creates clean, readable release Word document

Auto-creates Jira ticket with complete description

📚 Resources
GitHub REST API Docs

Jira Cloud REST API Docs

PyGithub Docs

Jira Python Library

ADF Format Docs

👨‍💻 Developed By
Yoseph Benchimol
Intern @ TelevisaUnivision
2025


