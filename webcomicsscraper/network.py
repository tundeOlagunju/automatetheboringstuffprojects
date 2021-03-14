import requests,bs4

def download_html(url):
    res = requests.get(url)
    html = bs4.BeautifulSoup(res.text, 'html.parser')
    res.raise_for_status()
    return html or ''
    
    