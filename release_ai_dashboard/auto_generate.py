import sys
from release_ai_dashboard.release_utils import get_release_data
from release_ai_dashboard.gpt_utils import (
    generate_release_doc_with_gpt,
    generate_professional_word
)
from release_ai_dashboard.adf_utils import build_rich_adf_description
from release_ai_dashboard.jira_utils import create_jira_ticket
from release_ai_dashboard.fetchers import fetch_jira_ticket_details  # Asegúrate de tener este archivo

def main(version_tag=None):
    if not version_tag:
        if len(sys.argv) != 2:
            print("Usage: python -m release_ai_dashboard.auto_generate <version_tag>")
            sys.exit(1)
        version_tag = sys.argv[1]

    print(f"🚀 Generating release for: {version_tag}")

    # 🔍 Get release notes and ticket IDs from GitHub
    release_notes, ticket_ids = get_release_data(version_tag)

    if not release_notes:
        print("❌ No release notes found. Aborting.")
        sys.exit(1)

    # 🔍 Get full details for each ticket from Jira
    tickets_info = [fetch_jira_ticket_details(tid) for tid in ticket_ids]

    # 🧱 Build the ADF description for Jira
    adf_description = build_rich_adf_description(release_notes, tickets_info)

    # 🧾 Create Jira ticket
    create_jira_ticket(version_tag, adf_description)
    print("✅ Jira ticket created successfully.")

if __name__ == "__main__":
    main()
