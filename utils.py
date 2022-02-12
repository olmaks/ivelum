import re

from regex_patterns import REGEXP_PATTERNS


def replace_content(text_content):
    """ Custom generator for generating formatted text """
    for text in text_content.split(' '):
        if not re.match(REGEXP_PATTERNS['is_url'], text):
            yield re.sub(REGEXP_PATTERNS['search_pattern'], '\\1™', text)
        else:
            yield text


def prepare_html_response(title, body):
    """Return base page structure"""
    return '<html><head>' \
           '<title>{}</title>' \
           '<body>{}</body>' \
           '</head></html>'.format(title, body)


def replace_url(api_url, url):
    if api_url in url:
        pattern = REGEXP_PATTERNS['url_replace']
        return re.sub(pattern, '/', url)


def is_url(url):
    return re.match(REGEXP_PATTERNS['is_url'], url)