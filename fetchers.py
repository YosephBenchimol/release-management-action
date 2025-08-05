import os
import requests
from requests.auth import HTTPBasicAuth

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = os.getenv("JIRA_BASE_URL")

def fetch_jira_ticket_details(ticket_id):
    url = f"{JIRA_URL}/rest/api/3/issue/{ticket_id}"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200:
        data = response.json()
        fields = data["fields"]
        return {
            "id": ticket_id,
            "summary": fields.get("summary", ""),
            "status": fields.get("status", {}).get("name", ""),
            "url": f"{JIRA_URL}/browse/{ticket_id}",
            "epic": fields.get("customfield_10014", "Other") or "Other"
        }

    return {
        "id": ticket_id,
        "summary": "Not found",
        "status": "Unknown",
        "url": f"{JIRA_URL}/browse/{ticket_id}",
        "epic": "Other"
    }
