import os

def get_release_notes(version_tag):
    print("⚠️ Saltando conexión real con GitHub. Usando release notes quemados.")

    return f"""
WebApp:
- [CWB-14201] Added new login flow for kids
- [CWB-14204] Updated paywall experience on iOS
- [CWB-14188] Fixed video player crash on Safari

Platform:
- [CWB-13992] Removed deprecated API for legacy content
- [CWB-14112] Improved homepage load performance
- [CWB-14003] Fixed broken deep link routing

[Release version: {version_tag}]
"""