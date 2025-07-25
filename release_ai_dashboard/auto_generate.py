import sys
import os
from dotenv import load_dotenv
from release_ai_dashboard.release_utils import get_release_data
from gpt_utils import generate_release_doc_with_gpt, generate_professional_word

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("❌ ERROR: Debes pasar el version tag como argumento. Ejemplo: python auto_generate.py v1.111.0")
        sys.exit(1)

    version_tag = sys.argv[1]
    print(f"🚀 Generando release para: {version_tag}")

    # 1. Obtener datos simulados (en tu caso aún no conectas GitHub)
    release_notes, tickets_info = get_release_data(version_tag)

    # 2. Generar contenido con GPT
    gpt_output = generate_release_doc_with_gpt(version_tag, release_notes, tickets_info)

    # 3. Crear Word document
    filename = generate_professional_word(version_tag, gpt_output)

    print(f"✅ Documento generado: {filename}")

if __name__ == "__main__":
    main()