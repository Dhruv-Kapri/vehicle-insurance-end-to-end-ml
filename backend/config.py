import os

from fastapi.templating import Jinja2Templates
from from_root import from_root

BASE_DIR = from_root()

static_dir_path = os.path.join(BASE_DIR, "frontend/static")
templates_dir_path = os.path.join(BASE_DIR, "frontend/templates")

templates = Jinja2Templates(directory=templates_dir_path)
