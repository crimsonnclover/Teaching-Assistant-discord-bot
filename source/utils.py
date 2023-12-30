import re


def get_channel(content: str) -> int:
    pattern = r'<#(\d+)>'
    match = re.match(pattern, content)

    if match: 
        return int(content[2:-1])
    else: 
        return None