import markdown
from bs4 import BeautifulSoup

def to_plain(md_text):
    parsed_html = markdown.markdown(md_text)
    result = BeautifulSoup(parsed_html, "html.parser").get_text()
    return result

