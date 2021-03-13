#! /usr/local/bin/python3
#gifdownloader.py - Opens several search results.
import  requests, sys, os, bs4, time, json
from selenium import webdriver


if len(sys.argv) < 2:
    print("View usage: Script requires search query")
    sys.exit()

SCROLL_PAUSE_TIME = 0.5
gif_search_query = ' '.join(sys.argv[1:])
URL = f'https://giphy.com/search/{gif_search_query}?sort=relevant'
giphy_gifs = 0

driver = webdriver.Chrome()
driver.get(URL) 
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# Scroll to the bottom until 25 relevant gifs are found or the bottom is reached
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Use selenium to download the page source as the content is dynamic
    html = driver.page_source
    soup = bs4.BeautifulSoup(html,'html.parser')
    gighy_grid = soup.find('div', attrs={'class': 'giphy-grid'})
    div_below_gighy_grid = gighy_grid.find('div')
    giphy_gifs = div_below_gighy_grid.find_all('a')

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height or len(giphy_gifs) >= 25:
        driver.quit()
        break
    last_height = new_height

if len(giphy_gifs) == 0:
    print(f"No gifs found for {gif_search_query}")

os.makedirs(gif_search_query, exist_ok=True)
for giphy_gif in giphy_gifs:
    res = requests.get(giphy_gif.get('href'))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    script = soup.select('script[name="giphy-schema"]')
    data = json.loads(script[0].string)
    gif_url = (data['image']['url'])
    print(f'Downloading gif {gif_url} ...')
    file_name = gif_url.split('/')[-2] 
    gif_file = os.path.join(gif_search_query, file_name+'.gif')
    with open(gif_file, 'wb') as f:
        f.write(requests.get(gif_url).content)
  