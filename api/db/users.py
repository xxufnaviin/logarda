import config.secrets
from utils.postgres import *
from utils.utils import *

conn = Postgres.create_connection()


def aws_keys_exists(username):
    if not config.secrets.AWS_ACCESS_KEY_ID:
        keys, empty = Postgres.get_aws_access_keys(conn, username)
        if empty:
            print("keys does not exist")
            return False
        
        set_aws_access_keys(keys)
    return True
