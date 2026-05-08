from utils.postgres import *
from logs.logs_collector import logs_collector
from metrics.metrics_collector import metrics_collector

conn = Postgres.create_connection()
users = Postgres.get_all_users(conn)

if __name__== "__main__":
    if users:
        for username in users:
            print(f"Collecting data for: {username}")
            metrics_collector(username)
            logs_collector(username)
            
    else:
        print("No users with data collector on.")


