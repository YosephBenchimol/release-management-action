import os
import re
from github import Github

def get_release_data(version_tag):
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")

    if not token or not repo_name:
        print("❌ No GITHUB_TOKEN o GITHUB_REPO configurado.")
        return "⚠️ Error de configuración", []

    g = Github(token)
    repo = g.get_repo(repo_name)

    try:
        release = repo.get_release(version_tag)
        current_tag = version_tag
        current_sha = repo.get_git_ref(f"tags/{current_tag}").object.sha
        current_commit = repo.get_commit(current_sha)

        # Buscar tag anterior por fecha
        all_tags = sorted(repo.get_tags(), key=lambda t: t.commit.commit.author.date)
        prev_tag = None
        for i in range(1, len(all_tags)):
            if all_tags[i].name == current_tag:
                prev_tag = all_tags[i - 1].name
                break

        if not prev_tag:
            print("⚠️ No se encontró un tag anterior. Usando últimos 50 commits.")
            commits = repo.get_commits(sha=current_sha)[:50]
        else:
            print(f"ℹ️ Comparando con tag anterior: {prev_tag}")
            prev_sha = repo.get_git_ref(f"tags/{prev_tag}").object.sha
            prev_commit = repo.get_commit(prev_sha)
            commits = repo.compare(prev_commit.sha, current_commit.sha).commits

        feature_keywords = ["add", "implement", "migrate", "refactor", "feature", "create"]
        bug_keywords = ["fix", "bug", "resolve", "patch", "error", "issue", "correct"]

        features = []
        bugs = []
        ticket_ids = set()

        for commit in commits:
            msg = commit.commit.message.strip()
            matches = re.findall(r"\[?(CWB|WEBTV)-\d+\]?", msg)
            full_ticket_ids = re.findall(r"(CWB-\d+|WEBTV-\d+)", msg)

            if not full_ticket_ids:
                continue

            ticket_ids.update(full_ticket_ids)

            line = f"- [{full_ticket_ids[0]}] {msg.splitlines()[0]}"
            lowered = msg.lower()
            if any(kw in lowered for kw in bug_keywords):
                bugs.append(line)
            elif any(kw in lowered for kw in feature_keywords):
                features.append(line)
            else:
                features.append(line)  # Default to feature

        # Armar release notes
        release_body = ""

        if features:
            release_body += "### Features\n" + "\n".join(features) + "\n\n"
        if bugs:
            release_body += "### Bug Fixes\n" + "\n".join(bugs) + "\n"

        if not release_body:
            release_body = "### No changes found in this release."

        print(f"✅ Release notes generados automáticamente. Tickets: {len(ticket_ids)}")

        return release_body, list(ticket_ids)

    except Exception as e:
        print(f"❌ Error al obtener data de GitHub: {e}")
        return "⚠️ Error al obtener datos de GitHub", []
