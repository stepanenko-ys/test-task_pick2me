# === For SQLite3 =============================================================
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASES_ENGINE = 'django.db.backends.sqlite3'
DATABASES_NAME = os.path.join(BASE_DIR, 'db.sqlite3')
# =============================================================================