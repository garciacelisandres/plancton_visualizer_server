from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def download(url, save_path, link_element_id):
    html = requests.get(url)
    if check_html(html):
        soup = BeautifulSoup(html.text, features="html.parser")
        bin_header = soup.find("a", {"id": link_element_id}).contents[0]
        download_url = parse_url(url, bin_header)
        download_zip(download_url, save_path)


def check_html(html):
    content_type = html.headers['Content-Type']
    if 'text/html' not in content_type:
        return False  # no HTML file
    if html.status_code != requests.codes.ok:
        return False  # error while requesting the HTML page
    return True


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


if __name__ == "__main__":
    download("https://ifcb-data.whoi.edu/timeline?dataset=mvco", "../", "bin-header")
