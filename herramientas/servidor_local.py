"""Sirve web/ en http://localhost:8940 igual que Vercel (/i/<n> muestra index.html)."""
import functools
import http.server
import os

WEB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web')


class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/i/') or self.path.split('?')[0] in ('/enviar',):
            self.path = '/index.html' if self.path.startswith('/i/') else '/enviar.html'
        return super().do_GET()


http.server.ThreadingHTTPServer(('127.0.0.1', 8940), functools.partial(H, directory=WEB)).serve_forever()
