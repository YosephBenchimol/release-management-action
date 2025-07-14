from flask import Flask, request, render_template, session, redirect, url_for
from datetime import timedelta
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gpt_utils import answer_question_with_gpt, compare_releases_with_gpt
from document_generator_ai import generate_structured_release_doc
from github_utils import get_release_data
from main import create_jira_issue, build_rich_adf_description, generate_friendly_summary

def parse_github_release_notes(release_notes):
    """
    Transforma el release.body plano de GitHub en una lista estructurada
    para usarla en generate_friendly_summary y otras funciones.
    """
    import re

    structured = []
    lines = release_notes.splitlines()

    current_section = None  # puede ser "feature" o "bug"

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detectar sección (Features o Bug Fixes)
        if "features" in line.lower():
            current_section = "feature"
            continue
        elif "bug fixes" in line.lower():
            current_section = "bug"
            continue

        # Saltar líneas de encabezado
        if line.startswith("#"):
            continue

        # Extrae el ticket si hay
        match = re.search(r'\b([A-Z]+-\d+)\b', line)
        ticket_id = match.group(1) if match else "UNKNOWN"

        # Si no hay sección detectada, hacer heurística
        l = line.lower()
        if current_section:
            item_type = current_section
        elif any(w in l for w in ['fix', 'bug', 'resolve']):
            item_type = 'bug'
        else:
            item_type = 'feature'

        structured.append({
            "type": item_type,
            "title": line[:80],
            "description": line,
            "ticket_id": ticket_id
        })

    return structured

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(hours=1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.args.get("reset") == "1":
        session.clear()
        return redirect(url_for("index"))

    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        action = request.form.get("action")

        if action == "generate":
            version_tag = request.form["tag"]
            release_date = "2025-06-23"
            github_link = f"https://github.com/televisa-univision/client-web/releases/tag/{version_tag}"

            # Crear subcarpeta si no existe
            release_dir = os.path.join("static", "releases")
            word_filename = f"{version_tag.replace('/', '-')}.docx"
            word_path = os.path.abspath(os.path.join(release_dir, word_filename))
            os.makedirs(os.path.dirname(word_path), exist_ok=True)

            # Obtener release notes reales desde GitHub
            real_notes = get_release_data(version_tag)

            # 🧩 Procesar tickets desde release notes
            structured_release_notes = parse_github_release_notes(real_notes)

            # 🧠 Generar resumen amigable con AI
            summary_text = generate_friendly_summary(version_tag, structured_release_notes)

            # 🧩 Preparar tickets para descripción ADF
            tickets_info = []
            for item in structured_release_notes:
                tickets_info.append({
                    "id": item["ticket_id"],
                    "summary": item["title"] + ": " + item["description"],
                    "status": "Ready",  # Este campo es opcional
                    "url": f"https://televisaunivision.atlassian.net/browse/{item['ticket_id']}"
                })

            # 🧾 Construir descripción ADF con summary incluido
            description_adf = build_rich_adf_description(real_notes, tickets_info, summary_text=summary_text)

            # 🏷️ Crear documento Word
            generate_structured_release_doc(word_path, {
                "project_name": "Client WebApp",
                "version": version_tag,
                "release_date": release_date,
                "prepared_by": "Yoseph Benchimol",
                "summary": [summary_text],
                "details": structured_release_notes,
                "known_issues": [],
                "checklist": [
                    "Código mergeado en rama main",
                    "Pruebas pasadas en staging",
                    "Lanzamiento a producción confirmado"
                ],
                "stakeholders": [
                    "Product Owner: Juan Pérez ✅",
                    "QA Lead: Ana Torres ✅",
                    "DevOps: Miguel Díaz ✅"
                ],
                "links": [
                    ("Release en GitHub", github_link),
                    ("Documentación técnica", "https://confluence.televisaunivision.com/display/PROJECTDOCS"),
                    ("Jira Board", "https://televisaunivision.atlassian.net/jira/software/c/projects/CWB/boards/34")
                ]
            })

            # 🪄 Crear ticket en Jira
            jira_key = create_jira_issue(f"Release Document for {version_tag}", description_adf, tickets_info, real_notes)

            # 💾 Guardar en sesión
            session['release'] = {
                "text": version_tag,
                "tag": version_tag,
                "word": f"releases/{word_filename}",
                "version": version_tag,
                "body": real_notes,
                "summary": [summary_text],
                "details": structured_release_notes,
                "known_issues": [],
                "ticket_url": f"https://televisaunivision.atlassian.net/browse/{jira_key}" if jira_key else None
            }

            session.setdefault('release_history', [])
            session['release_history'].append({
                "version": version_tag,
                "file": f"releases/{word_filename}",
                "date": release_date
            })
            session.modified = True

        elif action == "ask":
            question = request.form["question"]
            chat = session.get("chat_history", [])

            last_version = session.get("chat_release_version")
            current_version = session['release'].get("version")

            if last_version and last_version != current_version:
                chat.append({
                    "role": "assistant",
                    "content": f"🆕 You are now discussing release **{current_version}**."
                })

            session["chat_release_version"] = current_version
            chat.append({"role": "user", "content": question})

            release_info = {
                "version": session['release'].get("version", ""),
                "summary": session['release'].get("summary", []),
                "details": session['release'].get("details", []),
                "known_issues": session['release'].get("known_issues", []),
                "body": session['release'].get("body", "")
            }

            answer = answer_question_with_gpt(
                question=question,
                release_info=release_info,
                history=chat
            )

            chat.append({"role": "assistant", "content": answer})
            session['chat_history'] = chat
            session.modified = True

        elif action == "compare":
            tag_a = request.form["release_a"]
            tag_b = request.form["release_b"]

            release_a = {
                "version": tag_a,
                "summary": ["Mejoras en autenticación"],
                "details": [
                    {"ticket": "CWB-14000", "description": "Improved login security."}
                ],
                "known_issues": ["Bug con token en Firefox"]
            }

            release_b = {
                "version": tag_b,
                "summary": ["Optimización en login", "Reducción de latencia"],
                "details": [
                    {"ticket": "CWB-14001", "description": "Fixed latency issue."},
                    {"ticket": "CWB-14002", "description": "Patched Firefox token bug."}
                ],
                "known_issues": []
            }

            comparison = compare_releases_with_gpt(release_a, release_b)
            session["comparison_result"] = comparison
            session.modified = True

    return render_template("index.html",
                           release_text=session.get('release', {}).get("text"),
                           word_filename=session.get('release', {}).get("word"),
                           version_tag=session.get('release', {}).get("tag"),
                           chat_history=session.get("chat_history", []),
                           ticket_url=session.get('release', {}).get("ticket_url"),
                           release_history=session.get("release_history", []),
                           comparison_result=session.get("comparison_result"))

if __name__ == '__main__':
    app.run(debug=True)
