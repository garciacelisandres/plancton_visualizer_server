import threading
import time
from os import environ

from sample_download import download, load, predict
from database.database_api import init_db

from dotenv import load_dotenv
load_dotenv()


class BackgroundJob:
    def __init__(self, interval: int, daemon: bool):
        self.interval = interval
        self.last_downloaded_filename = None

        # Initialize the database
        init_db(
            environ.get("DATABASE_URL"),
            environ.get("DATABASE_NAME")
        )

        if daemon:
            self.thread = threading.Thread(target=self.run, args=())
            self.thread.daemon = True
            self.thread.start()
        else:
            self.run()

    def run(self):
        while True:
            (filename, content_downloaded) = download(
                environ.get("DOWNLOAD_URL"),
                environ.get("DOWNLOAD_SAVE_PATH"),
                self.last_downloaded_filename
            )
            if content_downloaded:
                load(filename, environ.get("LOAD_DESTINATION_DIR"))
                downloaded_filename = filename.split(".")[0]
                predict(downloaded_filename)
                self.last_downloaded_filename = downloaded_filename

            time.sleep(self.interval)


if __name__ == "__main__":
    BackgroundJob(1200, False)
