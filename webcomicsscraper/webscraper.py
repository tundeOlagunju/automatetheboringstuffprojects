from contentextractor import ContentExtractor
from fileutils import FileUtils
from webcomic import WebComicDownloadState, WebComicDownloaddata, WebComic

import logging
import jsonpickle

class WebComicScraper(object):

    def __init__(self, file_path):
        self.file_path = file_path
    
    def scrape(self):
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
        logging.info('Scraping has started')

        logging.info('Reading and deserializing input json %s', self.file_path)
        input_json = FileUtils.read_json_file(self.file_path)
        comic_download_data = FileUtils.decode_json(input_json)
        logging.info('Input json deserialized successfully. List of webcomics %s', [data.url for data in comic_download_data])
        

        for i, comicdata in enumerate(comic_download_data):
            webcomic = WebComic(comicdata)
            if comicdata == '' or comicdata == None:
                comicdata.last_download_state = WebComicDownloadState.FAILED_RESPONSE
                logging.info('Webcomic at position %s does not contain a url. Skipping..', i+1)
                continue

            logging.info('Downloading page %s ....', comicdata.url)
            webcomic.download()
            if webcomic.download_state != WebComicDownloadState.SUCCESS:
                logging.info('Skipping %s as page download was not successful', comicdata.url)
                continue
            logging.info('Page download successful for %s', comicdata.url)

            content_extractor = ContentExtractor(webcomic.comic_html)
            webcomic.extractor = content_extractor

            webcomic.extract_img_links()

        import sys
        print(sys.getrecursionlimit())
        sys.setrecursionlimit(15000)
        # print(webcomics)
        print(jsonpickle.encode(comic_download_data, unpicklable=False))
        

if __name__ == '__main__':
    comic_scraper = WebComicScraper('input.json')
    comic_scraper.scrape()
