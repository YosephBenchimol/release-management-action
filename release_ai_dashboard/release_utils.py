from github_utils import get_release_notes

def get_release_data(version_tag):
    """
    Devuelve los release notes desde GitHub y los tickets desde Jira (mock por ahora).
    """
    release_notes = get_release_notes(version_tag)

    # Por ahora, los tickets son simulados
    tickets_info = "Ticket info not yet connected"

    return release_notes, tickets_info