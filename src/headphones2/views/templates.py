import headphones2

from mako.lookup import TemplateLookup
from mako import exceptions
import os

TEMPLATE_DIR = os.path.join(headphones2.__path__[0], '..', 'frontend', 'interfaces', 'default')

import sys
sys.modules['headphones'] = headphones2


def serve_template(templatename, **kwargs):
    _hplookup = TemplateLookup(directories=[TEMPLATE_DIR])

    try:
        template = _hplookup.get_template(templatename)
        return template.render(**kwargs)
    except:
        return exceptions.html_error_template().render()

