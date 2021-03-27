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
        
        if not self.file_path:
            logging.debug('Exiting because json input file was not provided. Scraping did not start')
            exit()

        try:
            input_data = files.read_json_file(self.file_path)
        except Exception:
            logging.debug('Exiting because no data in the input file. Scraping did not start')
            exit()

        if not input_data:
            logging.debug('Exiting because no data in the input file. Scraping did not start')
            exit()

        logging.info('Input json contains List of webcomics %s', [ data['url'] for data in input_data])  
        logging.info('Scraping has started')

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
                output_data.append(webcomic.download_data)
                continue
            
            content_extractor = ContentExtractor(webcomic.comic_html, webcomic.download_data.url)
            webcomic.extractor = content_extractor

            webcomic.download_latest_image()
            webcomic.save_image()

            output_data.append(webcomic.download_data)

        output_json = jsonpickle.encode(output_data, unpicklable=False)
        files.save_json(self.file_path, output_json)
        logging.info('Output data saved successfully. Scraping has ended')
        

if __name__ == '__main__':
    comic_scraper = WebComicScraper('input.json')
    comic_scraper.scrape()
