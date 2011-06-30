from distutils import dir_util
from jinja2 import Environment, FileSystemLoader
import codecs
import os
import shutil

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

#
# configuration
#

OUTPUT_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'www'))

from conf import *

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# configure Jinja2

fsloader = FileSystemLoader(os.path.join(PROJECT_ROOT, 'src', 'templates'))
env = Environment(loader=fsloader)

# clean output dir

print "Cleaning output directory..."

for name in os.listdir(OUTPUT_DIR):
    path = os.path.join(OUTPUT_DIR, name)
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.unlink(path)

# generate pages

for page in PAGES:
    
    print "Generating %s..." % page
    
    template = env.get_template(page)
    rendered = template.render(**CONTEXT)
    
    outfile = codecs.open(os.path.join(OUTPUT_DIR, page), 'w', encoding='utf8')
    outfile.write(rendered)
    outfile.close()

# copy static media

print "Copying static assets..."

STATIC_PATH = os.path.join(PROJECT_ROOT, 'src', 'static')

for name in os.listdir(STATIC_PATH):
    src = os.path.join(STATIC_PATH, name)
    dst = os.path.join(OUTPUT_DIR, name)
    dir_util.copy_tree(src, dst)

print "Done!"