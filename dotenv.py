import os
from datetime import datetime

# not exist credentials file, then die
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'credentials')):
    print("❌ Credentials file not found")
    exit(1)

def get_credential(filename: str) -> str:
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'credentials')):
        print("❌ Credentials file not found")
        exit(1)
    return open(os.path.join(os.path.dirname(__file__), 'credentials', filename), 'r').read().strip()
    
def get_credential_if_exists(filename: str) -> str | None:
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'credentials')):
        return None
    return open(os.path.join(os.path.dirname(__file__), 'credentials', filename), 'r').read().strip()

INPUT_DIR = get_credential('input_dir.txt')
OUTPUT_PATH = get_credential('output_dir.txt')
AUTHOR = get_credential_if_exists('author.txt')

WEBSITE = get_credential_if_exists('website.txt')
EMAIL = get_credential_if_exists('email.txt')

LOG = True
LOG_JSON = False
ACCEPT_EXTENSION = ['jpg', 'jpeg', 'png', 'webp', 'heic', 'heif', 'gif', 'avif', 'svg']

GET_COPYRIGHT_INFO = get_credential_if_exists('copyright_info.txt')
# check if the copyright info is not empty, if it is not empty, then use it, otherwise use the default copyright info
COPYRIGHT_INFO = GET_COPYRIGHT_INFO if GET_COPYRIGHT_INFO else f"© {datetime.now().year} {AUTHOR}. All rights reserved."

GEMINI_API_KEY = get_credential('gemini_api_key.txt')

PROMPT = get_credential('prompt.txt')
MODEL = get_credential('model.txt')

IMAGE_DESCRIPTION_KEY:str = 'title' # title, description, subject, keywords
IMAGE_SUBJECT_KEY:str = 'title' # title, description, subject, keywords
REMOVE_BACKUP_FILE:bool = True