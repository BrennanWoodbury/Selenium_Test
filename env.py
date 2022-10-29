from os import environ as env
from dotenv import load_dotenv

load_dotenv()

# there are creds for Status.IO under epicor asset 'StatusIO'
status_io_username = env["status_io_username"]
status_io_password = env["status_io_password"]
download_path = env["download_path"]
path_to_logs = env["path_to_logs"]
email_username = env["email_username"]
email_password = env["email_password"]
smtp_server = env["smtp_server"]
