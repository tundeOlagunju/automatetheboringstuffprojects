from contentextractor import ContentExtractor
from fileutils import FileUtils
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

        logging.info('Reading and deserializing input json %s', self.file_path)
        input_json = FileUtils.read_json_file(self.file_path)
        comic_download_data = FileUtils.decode_json(input_json)
        logging.info('Input json contains List of webcomics %s', [data.url for data in comic_download_data])
        

        for i, comicdata in enumerate(comic_download_data):
            webcomic = WebComic(comicdata)
            if not comicdata:
                comicdata.last_download_status = WebComicDownloadStatus.FAILED.name
                logging.info('Webcomic at position %s does not contain a url. Skipping..', i+1)
                continue

            logging.info('Downloading page %s ....', comicdata.url)
            webcomic.download()
            if webcomic.download_data.last_download_status != WebComicDownloadStatus.SUCCESS.name:
                logging.info('Skipping %s as page download was not successful', comicdata.url)
                continue
            logging.info('Page download successful for %s', comicdata.url)

            content_extractor = ContentExtractor(webcomic.comic_html)
            webcomic.extractor = content_extractor

            logging.info('Extracting all image links in %s ....', comicdata.url)
            webcomic.fetch_img_urls()
            logging.info('Finished extracting all image links in %s successfully', comicdata.url)
            
            logging.info('Fetching the title in %s ....', comicdata.url)
            webcomic.fetch_title()

            # Theres still an edge case with title
            print(webcomic.title)
        

        print(jsonpickle.encode(comic_download_data, unpicklable=False))
        

if __name__ == '__main__':
    comic_scraper = WebComicScraper('input.json')
    comic_scraper.scrape()
