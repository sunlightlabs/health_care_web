from jinja2 import Environment, FileSystemLoader
from werkzeug.wrappers import Request, Response
import mimetypes
import os

from conf import *

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
STATIC_PATH = os.path.join(SRC_PATH, 'static')

fsloader = FileSystemLoader(os.path.join(SRC_PATH, 'templates'))
env = Environment(loader=fsloader)

@Request.application
def application(request):
    path = request.path.lstrip('/')
    if path == '':
        path = INDEX
    if path in PAGES:
        template = env.get_template(path)
        rendered = template.render(**CONTEXT)
        response = Response(rendered, content_type='text/html')
    else:
        filepath = os.path.abspath(os.path.join(STATIC_PATH, path))
        if not filepath.startswith(STATIC_PATH):
            response = Response('stop it')
            response.status_code = 404
        else:
            if os.path.exists(filepath):
                mimetype = mimetypes.guess_type(filepath)[0]
                infile = open(filepath)
                data = infile.read()
                infile.close()
                response = Response(data, content_type=mimetype)
            else:
                response = Response('not found')
                response.status_code = 404
    return response

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, application)