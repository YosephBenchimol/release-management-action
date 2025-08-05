import os
from github import Github

def get_release_notes(version_tag):
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO") or "televisa-univision/client-web"

    if not token:
        print("⚠️ No GITHUB_TOKEN configurado. Usando release notes quemados.")
        return f"""
### Features
- [CWB-14201] Added new login flow for kids
- [CWB-14204] Updated paywall experience on iOS

### Bug Fixes
- [CWB-14188] Fixed video player crash on Safari
- [CWB-13992] Removed deprecated API for legacy content
- [CWB-14112] Improved homepage load performance
- [CWB-14003] Fixed broken deep link routing
"""

    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        releases = repo.get_releases()

        for r in releases:
            if r.tag_name == version_tag:
                print(f"✅ Release encontrado: {r.tag_name}")
                return r.body or "⚠️ Release sin contenido."

        print(f"⚠️ Release con tag {version_tag} no encontrado.")
        return f"⚠️ No se encontró un release publicado para {version_tag}."

    except Exception as e:
        print(f"❌ Error al conectar con GitHub: {e}")
        return f"⚠️ No se pudo obtener el release real para {version_tag}."


