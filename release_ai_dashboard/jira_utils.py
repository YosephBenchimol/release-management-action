import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
PROJECT_KEY = "CWB"  # Puedes cambiar esto si usas otro proyecto en Jira

if not JIRA_EMAIL or not JIRA_API_TOKEN or not JIRA_BASE_URL:
    raise ValueError("❌ Missing one or more required JIRA environment variables.")

def create_jira_ticket(version_tag, adf_description):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },
            "summary": f"📘 Release Documentation - {version_tag}",
            "description": {
                "type": "doc",
                "version": 1,
                "content": adf_description["content"]
            },
            "issuetype": {
                "name": "Task"
            },
            "labels": ["release-documentation", "WebApp"]
        }
    }

    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))

    if response.status_code == 201:
        ticket_key = response.json().get("key")
        print(f"✅ Jira ticket creado: {ticket_key}")
        return ticket_key
    else:
        print(f"❌ Error al crear el ticket en Jira: {response.status_code}")
        print(response.text)
        raise Exception("Failed to create Jira ticket.")
