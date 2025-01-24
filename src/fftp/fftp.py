import os
import random
import string
import logging
import argparse
import signal
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('tempftp.log')
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class CustomFTPHandler(FTPHandler):
    def on_login(self, username):
        logging.info(f"User '{username}' logged in successfully.")

    def on_login_failed(self, username, password):
        logging.warning(f"Failed login attempt for user '{username}' with password '{password}'.")

    def on_file_received(self, file):
        logging.info(f"File received: {file}")

    def on_file_sent(self, file):
        logging.info(f"File sent: {file}")

    def on_file_deleted(self, file):
        logging.info(f"File deleted: {file}")

    def on_file_renamed(self, old_file, new_file):
        logging.info(f"File renamed from '{old_file}' to '{new_file}'")

    def on_file_downloaded(self, file):
        logging.info(f"File downloaded: {file}")

    def on_file_stored(self, file):
        logging.info(f"File stored: {file}")

    def on_file_retrieved(self, file):
        logging.info(f"File retrieved: {file}")

    def on_file_aborted(self, file):
        logging.info(f"File transfer aborted: {file}")

    def on_file_changed(self, file):
        logging.info(f"File changed: {file}")

    def on_file_moved(self, old_file, new_file):
        logging.info(f"File moved from '{old_file}' to '{new_file}'")

    def on_file_uploaded(self, file):
        logging.info(f"File uploaded: {file}")

    def on_connect(self):
        logger.info(f"Client connected: {self.remote_ip}")

    def on_disconnect(self):
        logger.info(f"Client disconnected: {self.remote_ip}")

    def on_logout(self, username):
        logger.info(f"User logged out: {username}")

    def on_incomplete_file_received(self, file):
        logger.warning(f"Incomplete file received: {file}")

    def on_incomplete_file_sent(self, file):
        logger.warning(f"Incomplete file received: {file}")

class TempFTPServer:
    def __init__(self, directory, port, allow_anonymous):
        self.directory = directory
        self.port = port
        self.allow_anonymous = allow_anonymous
        self.server = None

    def start(self):
        authorizer = DummyAuthorizer()

        # create random user
        username = self.generate_username()
        password = self.generate_password()
        authorizer.add_user(username, password, self.directory, perm='elradfmwMT')
        logging.info(f"Temporary user created: '{username}' with password '{password}'")

        # anonymous user if set
        if self.allow_anonymous:
            authorizer.add_anonymous(self.directory)

        handler = CustomFTPHandler
        handler.authorizer = authorizer

        self.server = ThreadedFTPServer(("", self.port), handler)
        logging.info(f"Starting FTP server on port {self.port}")

        self.server.serve_forever()

    def cleanup(self):
        logging.info("Shutting down FTP server...")
        if self.server:
            self.server.close_all()
        logging.info("FTP server shut down.")

    @staticmethod
    def generate_username(length=8):
        return ''.join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def generate_password(length=12):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def signal_handler(sig, frame):
    logging.info("Received Ctrl+C, shutting down...")
    ftp_server.cleanup()
    exit(0)

def main():
    parser = argparse.ArgumentParser(description='Temporary FTP Server')
    parser.add_argument('--dir', required=True, help='Directory to serve files from')
    parser.add_argument('--port', type=int, default=21, help='Port to run the FTP server on')
    parser.add_argument('--anonymous', action='store_true', help='Allow anonymous FTP access')

    args = parser.parse_args()

    if not os.path.exists(args.dir):
        print(f"Error: The directory '{args.dir}' does not exist.")
        return

    global ftp_server
    ftp_server = TempFTPServer(args.dir, args.port, args.anonymous)
    signal.signal(signal.SIGINT, signal_handler)
    ftp_server.start()

if __name__ == "__main__":
    main()

