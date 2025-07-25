from release_ai_dashboard.github_utils import get_release_notes

def get_release_data(version_tag):
    release_notes = get_release_notes(version_tag)
    tickets_info = "Ticket info not yet connected"
    return release_notes, tickets_info