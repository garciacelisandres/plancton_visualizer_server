import threading
import time
from os import environ

from sample_download import download, load, predict
from database.database_api import get_db


class BackgroundJob:
    def __init__(self, interval: int):
        self.interval = interval

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            print("download")
            print("load")
            print("predict")
            filename = download(
                environ.get("DOWNLOAD_URL"),
                environ.get("DOWNLOAD_SAVE_PATH"),
                environ.get("DOWNLOAD_LINK_ELEMENT_ID"))
            load(filename, environ.get("LOAD_DESTINATION_DIR"))
            predict(filename.split(".")[0], get_db())

            time.sleep(self.interval)
