def build_rich_adf_description(version_tag, gpt_output):
    """
    Convierte el texto GPT (markdown) en formato ADF para Jira
    """
    def markdown_to_adf(text):
        lines = text.strip().split("\n")
        content = []

        for line in lines:
            line = line.strip()
            if not line:
                content.append({
                    "type": "paragraph",
                    "content": [{"type": "text", "text": ""}]
                })
                continue

            if line.startswith("# "):
                content.append({
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": [{"type": "text", "text": line[2:].strip()}]
                })
            elif line.startswith("## "):
                content.append({
                    "type": "heading",
                    "attrs": {"level": 2},
                    "content": [{"type": "text", "text": line[3:].strip()}]
                })
            elif line.startswith("- [") and "](" in line:
                import re
                match = re.match(r"- \[(.*?)\]\((.*?)\): (.*)", line)
                if match:
                    key, url, desc = match.groups()
                    content.append({
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"{key}: ",
                                "marks": [{"type": "link", "attrs": {"href": url}}]
                            },
                            {"type": "text", "text": desc}
                        ]
                    })
                else:
                    content.append({
                        "type": "paragraph",
                        "content": [{"type": "text", "text": line}]
                    })
            elif line.startswith("- "):
                content.append({
                    "type": "bulletList",
                    "content": [{
                        "type": "listItem",
                        "content": [{
                            "type": "paragraph",
                            "content": [{"type": "text", "text": line[2:].strip()}]
                        }]
                    }]
                })
            else:
                content.append({
                    "type": "paragraph",
                    "content": [{"type": "text", "text": line}]
                })

        return content

    return {
        "version": 1,
        "type": "doc",
        "content": markdown_to_adf(gpt_output)
    }
