from dotenv import load_dotenv
from os import path

ROOT_DIR = path.abspath(path.join(path.dirname(__file__), "..", ".."))
ENV_FILE = path.join(ROOT_DIR, ".env")

load_dotenv(ENV_FILE)