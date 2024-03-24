import re

def build_full_name(title: str, first_name: str, last_name: str) -> str:
    if title is None:
        return first_name.strip() + " " + last_name.strip()
    else:
        return title.strip() + " " + first_name.strip() + " " + last_name.strip()
      
def strip_multiline_text(multiline_text: str) -> str:
    return re.sub(r'\s+', ' ', multiline_text.replace("\n", ""))