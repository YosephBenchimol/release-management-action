import sys
from release_utils import get_release_data
from gpt_utils import (
    generate_release_doc_with_gpt,
    generate_professional_word
)
from adf_utils import build_rich_adf_description
from jira_utils import create_jira_ticket

def main():
    if len(sys.argv) != 2:
        print("Usage: python auto_generate.py <version_tag>")
        sys.exit(1)

    version_tag = sys.argv[1]
    print(f"🚀 Generando release para: {version_tag}")

    # 🔥 Obtener release notes y tickets (usa datos quemados si no hay API)
    release_notes, tickets_info = get_release_data(version_tag)

    # 🧠 Generar contenido usando GPT
    gpt_output = generate_release_doc_with_gpt(version_tag, release_notes, tickets_info)

    # 📄 Crear documento Word
    docx_filename = generate_professional_word(version_tag, gpt_output)
    print(f"✅ Documento Word generado: {docx_filename}")

    # 🧱 Crear descripción en ADF para Jira
    adf_description = build_rich_adf_description(version_tag, gpt_output)

    # 🧾 Crear ticket en Jira
    create_jira_ticket(version_tag, adf_description)

if __name__ == "__main__":
    main()