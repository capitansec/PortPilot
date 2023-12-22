import datetime
import os

from dotenv import load_dotenv

load_dotenv()


def log_writer(log, level):
    log_file_path = f"{os.getenv('LOG_FILE_PATH')}/{datetime.datetime.now().strftime('%Y-%m-%d')}.log"

    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as fp:
            pass

    with open(log_file_path, mode='a+') as f:
        content = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [{level.upper()}] {log}"
        f.write(content + '\n')
        f.close()
