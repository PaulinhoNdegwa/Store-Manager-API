from dotenv import load_dotenv
import os


def load_env_var():
    """Load dotenv variables"""
    APP_ROOT = os.path.join(os.path.dirname(__file__), "..")
    path_to_env = os.path.join(APP_ROOT, ".env")
    load_dotenv(path_to_env)
    print(os.getenv("DATABASE_URL"))
