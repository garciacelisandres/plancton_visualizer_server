from urllib.parse import urlparse

import requests
from json import loads

from database import get_db


def download(url: str, save_path: str, last_downloaded_filename: str or None) -> (
        str or None, bool):
    res = requests.get(url)
    if check_response(res):
        bin_header = loads(res.text)["bin_id"]
        check_already_downloaded(bin_header, last_downloaded_filename)
        download_url = parse_url(url, bin_header)
        filename = download_zip(download_url, save_path)
        return filename, True
    else:
        return None, False


def check_response(res):
    content_type = res.headers['Content-Type']
    if 'application/json' not in content_type:
        return False  # no HTML file
    if res.status_code != requests.codes.ok:
        return False  # error while requesting the HTML page
    return True


def check_already_downloaded(to_download_filename, last_downloaded_filename):
    if last_downloaded_filename:
        if to_download_filename == last_downloaded_filename:
            return True
    return get_db().find_sample_by_name(to_download_filename)


def parse_url(url, link):
    components = urlparse(url)
    scheme = components[0]
    netloc = components[1]
    final_url = '%s://%s/%s' % (scheme, netloc, "mvco/" + link + ".zip")
    return str(final_url)


def download_zip(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    save_path = save_path + url.split("/")[-1]
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
    return save_path
