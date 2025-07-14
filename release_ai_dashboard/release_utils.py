def get_release_data():
    release_notes = """
### Features
- [CWB-14400] New carousel added to homepage
- [CWB-14410] Improved video playback performance

### Bug Fixes
- [CWB-14390] Fixed login redirect bug
"""
    tickets_info = """
CWB-14400: Implemented new homepage carousel. Status: Done.
CWB-14410: Optimized video buffers for smoother playback. Status: Done.
CWB-14390: Login redirect caused blank page. Fixed. Status: Done.
"""
    return release_notes, tickets_info
