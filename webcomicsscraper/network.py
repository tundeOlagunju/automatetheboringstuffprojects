import requests,bs4, logging
import files, urls

def download_html(url):
    res = requests.get(url)
    html = bs4.BeautifulSoup(res.text, 'html.parser')
    res.raise_for_status()
    return html or ''
    

def download_image(img_url):
    prep_url = urls.prepare_img_url(img_url)
    print("prep_url", prep_url)
    res = requests.get(prep_url)
    res.raise_for_status()
    return res.content