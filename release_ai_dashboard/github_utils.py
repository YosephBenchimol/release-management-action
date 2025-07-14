import os
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # formato: "televisa-univision/client-web"

g = Github(GITHUB_TOKEN)

def get_release_data(tag):
    """
    Returns the body of the release for a given tag from GitHub.
    If the body is empty, it returns a list of recent commit messages as fallback.
    """
    try:
        repo = g.get_repo(GITHUB_REPO)
    except Exception as e:
        print("❌ ERROR: No se pudo acceder al repositorio.")
        print(e)
        return ""

    try:
        release = repo.get_release(tag)
        if release.body and release.body.strip():
            return release.body.strip()
    except Exception as e:
        print(f"⚠️ Release no encontrado para tag {tag}. Usando fallback de commits...")

    # Fallback: Buscar mensajes de commit recientes si no hay release.body
    try:
        commits = repo.get_commits()
        messages = []
        for commit in commits[:20]:
            msg = commit.commit.message.strip()
            if msg:
                messages.append(msg)
        return "\n".join(messages)
    except Exception as e:
        print("❌ ERROR: No se pudieron obtener los commits.")
        print(e)
        return ""
