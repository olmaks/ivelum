from socketserver import ThreadingMixIn
from urllib.error import HTTPError
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler, HTTPServer

from lxml.html import fromstring, tostring


class WebHandler(SimpleHTTPRequestHandler):
    API_URL = 'https://news.ycombinator.com/'
    DEFAULT_ENCODING = 'utf-8'
    REQUIRED_LENGTH = 6

    def do_GET(self):
        """Serve a GET request."""
        url = self.API_URL + self.path[1:]
        self.send_response(200)
        self.end_headers()
        try:
            with urlopen(url) as response:
                content_header = response.getheader('Content-Type')
                content, *charset = content_header.split('; charset=')
                charset = charset[0] if charset else self.DEFAULT_ENCODING
                # Skip not html files (image/gif, application/javascript etc.)
                if content == 'text/html':
                    page = response.read().decode(charset)
                    self.wfile.write(self.add_tm(page))
                else:
                    self.copyfile(urlopen(url), self.wfile)
        except HTTPError as http_error:
            title = 'Ooops'
            body = '<div>{}</div>'.format(http_error)
            html_response = self.prepare_html_response(title, body)
            self.wfile.write(bytes(html_response, self.DEFAULT_ENCODING))

    def add_tm(self, page):
        """Parse html page and add required sign"""
        root = fromstring(page)
        root_elements = [el for el in root.getiterator() if el.text]
        elements = [el for el in root_elements if el.text.strip()]
        for el in elements:
            # el.text doesn't return full html tag, use el.text_content() instead
            text_content = el.text_content()
            text = [t if len(t) != self.REQUIRED_LENGTH else t + '™'
                    for t in text_content.split(' ')]
            text = ' '.join(text)
            if text == text_content:
                continue
            parent = el.getparent()
            new_el = fromstring(text)
            new_el.tag = el.tag
            for k, v in el.attrib.items():
                new_el.attrib[k] = v
            parent.replace(el, new_el)
        return tostring(root)

    @staticmethod
    def prepare_html_response(title, body):
        """Return base page structure"""
        return '<html><head>' \
               '<title>{}</title>' \
               '<body>{}</body>' \
               '</head></html>'.format(title, body)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
