from github import Github
import os

def get_release_notes(version_tag):
    github_token = os.getenv("TOKEN_GITHUB_PUBLISH")
    repo_name = os.getenv("REPO_NAME", "YosephBenchimol/release-agent")

    if not github_token:
        raise ValueError("TOKEN_GITHUB_PUBLISH is not set")

    g = Github(github_token)
    repo = g.get_repo(repo_name)

    try:
        release = repo.get_release(version_tag)
        release_notes = release.body or "No release notes found"
        print("✅ Release notes loaded from GitHub")
    except Exception as e:
        release_notes = f"❌ Error fetching release notes: {e}"
        print(release_notes)

    return release_notes