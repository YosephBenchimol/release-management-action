# 📄 Release Management Documentation Agent

Automated Python-based tool that extracts release notes from GitHub, enriches them with Jira ticket data, generates a polished Word document, and creates a Jira ticket containing the release documentation using Atlassian ADF format.

---

## 🚀 Features

- 🔍 Auto-fetch GitHub Releases by version tag  
- 🔗 Integrates with Jira API to enrich notes with ticket data  
- 📝 Generates a professional Word document with structured release notes  
- 🤖 AI-powered executive summary for each release  
- 🧠 Interactive Q&A Chat to ask about specific release content  
- 🧾 Creates Jira tickets with formatted release documentation in ADF (Atlassian Document Format)  
- 🧪 Compare releases side-by-side to analyze key changes  

---

## 🧰 Tech Stack

- Python 3.11+  
- Flask – Web interface  
- GitHub API – Fetch release info, commits, and PRs  
- Jira API – Enrich tickets and create formatted issues  
- OpenAI API – AI-generated summaries and Q&A  
- python-docx – Generate Word documents  
- ADF JSON – Atlassian Document Format builder  

---

## 📦 Installation

```bash
git clone https://github.com/televisa-univision/web-release-integration.git
cd web-release-integration
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

⚙️ Environment Setup
Create a .env file in the root folder with:

ini
Copy
Edit
GITHUB_TOKEN=your_github_token
JIRA_EMAIL=your_email
JIRA_API_TOKEN=your_jira_token
JIRA_BASE_URL=https://yourdomain.atlassian.net
OPENAI_API_KEY=your_openai_key

▶️ Running the App
bash
Copy
Edit
python app.py
Open your browser at http://localhost:5000 to use the interface.

✅ GitHub Actions
This project includes a GitHub Action to automatically run and validate releases when new changes are pushed. See .github/workflows/python-app.yml.

📁 Project Structure
bash
Copy
Edit
release-agent/
│
├── app.py                  # Main Flask app
├── requirements.txt
├── document_generator_ai.py
├── gpt_utils.py
├── jira_utils.py
├── github_utils.py
├── templates/
│   └── index.html          # Web UI
├── static/
│   └── styles.css          # UI Styling
└── .github/workflows/
    └── python-app.yml      # GitHub Action config

📌 Use Case
This tool is ideal for:
- Engineering/Product teams managing frequent releases

- Automating Jira ticket creation with polished documentation

- Generating executive summaries with AI

- Keeping release communications consistent and professional

👨‍💻 Author
Yoseph Benchimol
Intern at TelevisaUnivision
Email: yosephbenchi@gmail.com

📜 License
MIT License