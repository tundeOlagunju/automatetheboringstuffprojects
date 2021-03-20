from contentextractor import ContentExtractor
import files
from webcomic import WebComicDownloadStatus, WebComicDownloaddata, WebComic

import logging
import jsonpickle
import sys

class WebComicScraper(object):

    def __init__(self, file_path):
        self.file_path = file_path
    
    def scrape(self):
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
        logging.info('Scraping has started')
        
        input_json = files.read_json_file(self.file_path)
        comic_download_data = files.decode_json(input_json)
        logging.info('Input json contains List of webcomics %s', [data.url for data in comic_download_data])
        

        for i, comicdata in enumerate(comic_download_data):
            if not comicdata.url:
                comicdata.last_download_status = WebComicDownloadStatus.FAILED.name
                logging.info('Webcomic at position %s does not contain a url. Skipping..', i+1)
                continue

            webcomic = WebComic(comicdata)
            webcomic.download_page()

            if webcomic.download_data.last_download_status != WebComicDownloadStatus.SUCCESS.name:
                logging.info('Skipping %s as page download was not successful', comicdata.url)
                continue
            
            content_extractor = ContentExtractor(webcomic.comic_html)
            webcomic.extractor = content_extractor
            webcomic.download_latest_image() 
            webcomic.save_image()

        print(jsonpickle.encode(comic_download_data, unpicklable=False))
        

if __name__ == '__main__':
    comic_scraper = WebComicScraper('input.json')
    comic_scraper.scrape()
