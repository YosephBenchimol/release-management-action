import sys
from release_ai_dashboard.release_utils import get_release_data
from release_ai_dashboard.gpt_utils import (
    generate_release_doc_with_gpt,
    generate_professional_word
)
from release_ai_dashboard.adf_utils import build_rich_adf_description
from release_ai_dashboard.jira_utils import create_jira_ticket

def main(version_tag=None):
    if not version_tag:
        if len(sys.argv) != 2:
            print("Usage: python -m release_ai_dashboard.auto_generate <version_tag>")
            sys.exit(1)
        version_tag = sys.argv[1]

    print(f"🚀 Generating release for: {version_tag}")

    # 🔍 Get release notes and tickets
    release_notes, tickets_info = get_release_data(version_tag)

    if not release_notes:
        print("❌ No release notes found. Aborting.")
        sys.exit(1)

    # 🔒 AI/Word Disabled – GPT generation and Word export are skipped
    # 🤖 gpt_output = generate_release_doc_with_gpt(version_tag, release_notes, tickets_info)
    # 📄 docx_filename = generate_professional_word(version_tag, gpt_output)
    # print(f"✅ Word document generated: {docx_filename}")

    # 🧱 Use GitHub release notes instead of AI to build ADF
    adf_description = build_rich_adf_description(release_notes, tickets_info)

    # 🧾 Create Jira ticket
    create_jira_ticket(version_tag, adf_description)
    print("✅ Jira ticket created successfully.")

if __name__ == "__main__":
    main()
