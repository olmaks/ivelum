from socketserver import ThreadingMixIn
from urllib.error import HTTPError
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler, HTTPServer

from lxml.html import fromstring, tostring

from utils import replace_url, is_url, replace_content


class WebHandler(SimpleHTTPRequestHandler):
    API_URL = 'news.ycombinator.com'
    API_URL_WITH_ENCRYPTION = 'https://{}/'.format(API_URL)
    DEFAULT_ENCODING = 'utf-8'
    REQUIRED_LENGTH = 6

    def do_GET(self):
        """Serve a GET request."""
        url = self.API_URL_WITH_ENCRYPTION + self.path[1:]
        try:
            with urlopen(url) as response:
                content_header = response.getheader('Content-Type')
                content, *charset = content_header.split('; charset=')
                charset = charset[0] if charset else self.DEFAULT_ENCODING
                # Skip not html files (image/gif, application/javascript etc.)
                self.send_response(200)
                self.end_headers()
                if content == 'text/html':
                    page = response.read().decode(charset)
                    self.wfile.write(self.add_tm(page))
                else:
                    self.copyfile(urlopen(url), self.wfile)
        except HTTPError as http_error:
            self.send_response(http_error.status)
            self.end_headers()
            self.wfile.write(http_error.read())

    def add_tm(self, page):
        """Parse html page and add required sign"""
        root = fromstring(page)
        self.link_parser(root)
        root_elements = [el for el in root.getiterator() if el.text]
        elements = [el for el in root_elements if el.text.strip()]
        for el in elements:
            if el.tag == 'a' and is_url(el.text_content()):
                continue
            text_content = el.text
            text = ' '.join(replace_content(text_content))
            if text == text_content:
                continue
            el.text = text
        return tostring(root)

    def link_parser(self, root):
        """ Replace API url into local. Modification from lxml rewrite_links"""
        for el, attrib, link, pos in root.iterlinks():
            if el.tag == 'a' and self.API_URL in link:
                new_link = replace_url(self.API_URL, link)
                if new_link == link:
                    continue
                cur = el.get(attrib)
                if not pos and len(cur) == len(link):
                    new = new_link
                else:
                    new = cur[:pos] + new_link + cur[pos + len(link):]
                el.set(attrib, new)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
