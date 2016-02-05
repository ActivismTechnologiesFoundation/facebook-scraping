import os

from . import create_app

app = create_app(os.getenv("ASSEMBLE_CONFIG") or 'default')
