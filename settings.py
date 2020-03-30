import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'

load_dotenv()
load_dotenv(dotenv_path=str(env_path), verbose=True)


username = os.getenv("GITHUB_USERNAME")
password = os.getenv("GITHUB_PASSWORD")