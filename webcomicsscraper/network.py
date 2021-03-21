import requests,bs4, logging
import urls

def download_html(url):
    res = requests.get(url)
    html = bs4.BeautifulSoup(res.text, 'html.parser')
    res.raise_for_status()
    return html
    

def download_image(img_url, url):
    """Tries to download the image with the given img url, if that fails, the image url is then refined further"""

    try_raw_url = None
    try:
        res = requests.get(img_url)
        try_raw_url = res.status_code == 200
    except Exception as e:
        logging.debug('Exception occured while trying to download image because of %s', e)

    if not try_raw_url:
        prep_url = urls.prepare_img_url(img_url, url)
        res = requests.get(prep_url)

    res.raise_for_status()
    return res.content