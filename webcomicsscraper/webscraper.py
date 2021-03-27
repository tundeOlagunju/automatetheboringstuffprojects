from contentextractor import ContentExtractor
import files
from webcomic import WebComicDownloadStatus, WebComicDownloaddata, WebComic

import logging
import jsonpickle
import sys, json

class WebComicScraper(object):

    def __init__(self, file_path):
        self.file_path = file_path
    
    def scrape(self):
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
        logging.info('Scraping has started')
        
        input_data = files.read_json_file(self.file_path)
        logging.info('Input json contains List of webcomics %s', [ data['url'] for data in input_data])
        
        output_data = []
        for i, comic_data in enumerate(input_data):
            if not 'url' in comic_data:
                logging.info('Webcomic at position %s does not contain a url. Skipping..', i+1)
                continue

            webcomic = WebComic()
            download_data = WebComicDownloaddata(comic_data)
            webcomic.download_data = download_data 

            webcomic.download_page()
            if webcomic.page_download_status != WebComicDownloadStatus.SUCCESS.name:
                logging.info('Skipping %s as page download was not successful', comic_data['url'])
                continue
            
            content_extractor = ContentExtractor(webcomic.comic_html, webcomic.download_data.url)
            webcomic.extractor = content_extractor

            webcomic.download_latest_image() 
            webcomic.save_image()
            output_data.append(webcomic.download_data)

        print(jsonpickle.encode(output_data, unpicklable=False))
        

if __name__ == '__main__':
    comic_scraper = WebComicScraper('input.json')
    comic_scraper.scrape()
