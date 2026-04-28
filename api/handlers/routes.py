import subprocess
import db.users
import config.secrets
from utils.utils import decrypt

def login():
    pass

# trigger data collection for user
def run_collectors(username):
    if db.users.aws_keys_exists(username):
        subprocess.run(["bash", "scripts/start_ingestion.sh", username], shell=True)
    


run_collectors("hey")