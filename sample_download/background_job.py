import threading
import time
from os import environ

from sample_download import download, load, predict


class BackgroundJob:
    def __init__(self, interval: int):
        self.interval = interval
        self.last_downloaded_filename = None

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            (filename, content_downloaded) = download(
                environ.get("DOWNLOAD_URL"),
                environ.get("DOWNLOAD_SAVE_PATH"),
                environ.get("DOWNLOAD_LINK_ELEMENT_ID"),
                self.last_downloaded_filename
            )
            if content_downloaded:
                load(filename, environ.get("LOAD_DESTINATION_DIR"))
                downloaded_filename = filename.split(".")[0]
                predict(downloaded_filename)
                self.last_downloaded_filename = downloaded_filename

            time.sleep(self.interval)
