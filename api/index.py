import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_portfolio.settings")

import django

django.setup()

# Initialize SQLite database on Vercel
if os.environ.get("VERCEL") == "1":
    from django.core.management import call_command

    try:
        call_command("migrate", interactive=False, verbosity=0)
    except Exception as exc:
        print(f"Migration warning: {exc}")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()