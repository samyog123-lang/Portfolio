import os
import sys
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_portfolio.settings")

# Vercel uses a temporary writable filesystem.
# Copy the committed SQLite database before Django starts.
source_db = BASE_DIR / "db.sqlite3"
target_db = Path("/tmp/db.sqlite3")

if source_db.exists() and not target_db.exists():
    shutil.copy2(source_db, target_db)

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()