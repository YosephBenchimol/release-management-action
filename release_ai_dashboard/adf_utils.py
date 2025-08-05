import re

def build_rich_adf_description(release_body, tickets_info):
    def make_link(text, url):
        return {
            "type": "text",
            "text": text,
            "marks": [{"type": "link", "attrs": {"href": url}}]
        }

    content = []

    # Header
    content.append({
        "type": "heading",
        "attrs": {"level": 2},
        "content": [{"type": "text", "text": "📦 Release Notes"}]
    })

    lines = release_body.splitlines()
    features, bugs = [], []
    current = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("### features"):
            current = "features"
            continue
        elif line.lower().startswith("### bug fixes"):
            current = "bugs"
            continue
        if current == "features":
            features.append(line)
        elif current == "bugs":
            bugs.append(line)

    def render_section(title, lines):
        content.append({
            "type": "heading",
            "attrs": {"level": 3},
            "content": [{"type": "text", "text": title}]
        })

        seen_blockcards = set()

        for line in lines:
            paragraph = {"type": "paragraph", "content": []}

            ticket_matches = re.findall(r"\b(WEBTV-\d+|CWB-\d+)\b", line)
            commit_links = re.findall(r"\((https:\/\/github\.com\/[^\s]+\/commit\/[a-f0-9]{7,40})\)", line)
            pr_links = re.findall(r"\((https:\/\/github\.com\/[^\s]+\/pull\/\d+)\)", line)

            # Clean text
            clean_text = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
            clean_text = re.sub(r"\[(WEBTV-\d+|CWB-\d+)\]", "", clean_text)
            clean_text = re.sub(r"\(https?:\/\/[^\s)]+\)", "", clean_text)
            clean_text = re.sub(r"https?:\/\/[^\s]+", "", clean_text)
            clean_text = re.sub(r"[\[\]()]", "", clean_text)
            clean_text = re.sub(r"^[•\-\.\s:—]+", "", clean_text).strip()

            if not clean_text:
                continue
            if not clean_text.endswith("."):
                clean_text += "."

            # Bullet
            paragraph["content"].append({"type": "text", "text": f"• {clean_text} "})

            # Links
            for t in ticket_matches:
                paragraph["content"].append(make_link(f"🔗 {t}", f"https://televisaunivision.atlassian.net/browse/{t}"))
            if pr_links:
                paragraph["content"].append({"type": "text", "text": " – "})
                paragraph["content"].append(make_link("[PR]", pr_links[0]))
            if commit_links:
                paragraph["content"].append({"type": "text", "text": " "})
                paragraph["content"].append(make_link("[Code]", commit_links[0]))

            content.append(paragraph)

            # Add blockCards with spacing (no duplicates)
            for t in ticket_matches:
                if t not in seen_blockcards:
                    content.append({"type": "paragraph", "content": []})  # spacing
                    content.append({
                        "type": "blockCard",
                        "attrs": {
                            "url": f"https://televisaunivision.atlassian.net/browse/{t}"
                        }
                    })
                    seen_blockcards.add(t)

    if features:
        render_section("🚀 Features", features)
    if bugs:
        render_section("🐞 Bug Fixes", bugs)

    # Summary block
    content.append({
        "type": "heading",
        "attrs": {"level": 3},
        "content": [{"type": "text", "text": "📌 Summary"}]
    })
    content.append({
        "type": "paragraph",
        "content": [{"type": "text", "text": f"• {len(features)} features delivered 🚀"}]
    })
    content.append({
        "type": "paragraph",
        "content": [{"type": "text", "text": f"• {len(bugs)} bugs resolved 🐞"}]
    })
    content.append({
        "type": "paragraph",
        "content": [{"type": "text", "text": "• 0 known issues ⚠️"}]
    })

    return {
        "type": "doc",
        "version": 1,
        "content": content
    }
