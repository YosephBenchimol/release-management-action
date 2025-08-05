import os
from github import Github

def get_release_notes(version_tag):
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")

    if not token or not repo_name:
        print("⚠️ No GITHUB_TOKEN o GITHUB_REPO configurado. Usando release notes quemados.")
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
        release = repo.get_release(version_tag)
        print(f"✅ Release encontrado: {release.tag_name}")
        return release.body or "⚠️ Release sin contenido."
    except Exception as e:
        print(f"❌ Error al conectar con GitHub: {e}")
        return "⚠️ No se pudo obtener el release real."
