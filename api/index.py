import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.backend.app import app  # noqa: E402,F401 — runtime Python do Vercel espera `app` no módulo
