import os
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("FLASK_ENV", "testing")
