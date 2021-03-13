import jsonpickle
from random import random
import network
import logging


class WebComicDownloadState(object):
    NOT_STARTED = 0
    FAILED_RESPONSE = 1
    SUCCESS = 2



class WebComicDownloaddata(object):
    def __init__(self):
        self.url = ''
        self._last_downloaded_image_link = ''
        self.last_tried = ''
        self.last_download_state = WebComicDownloadState.NOT_STARTED
        self.cache = ''
    
    @property
    def last_downloaded_image_link(self):
        return self._last_downloaded_image_link
    
    @last_downloaded_image_link.setter  
    def last(self, current_img_link):
        if current_img_link and current_img_link != self._last_downloaded_image_link : 
            self._last  = current_img_link




class WebComic(object):
    def __init__(self, download_data):
        self._comic_html = ''
        self._extractor = None
        self.img_links = []
        self.title = ''
        self.download_data = download_data
        self.download_data.last_download_state = WebComicDownloadState.NOT_STARTED

    @property
    def extractor(self):
        return self._extractor

    @extractor.setter
    def extractor(self, content_extractor):
        #check if downloaded first
        if self.comic_html:
            self._extractor = content_extractor
    
    @property
    def comic_html(self):
        return self._comic_html
    
    @comic_html.setter
    def comic_html(self, comic_html):
        if comic_html:
            self._comic_html = comic_html
            self.download_data.last_download_state = WebComicDownloadState.SUCCESS
        else: 
            self.download_data.last_download_state = WebComicDownloadState.FAILED_RESPONSE
            logging.debug('Html content is empty')

    def download(self):
        """Downloads the comic url's HTML content"""
        try:
            html = network.download_html(self.download_data.url)
            self.comic_html = html
        except Exception as e:
            self.download_data.last_download_state = WebComicDownloadState.FAILED_RESPONSE
            logging.debug('Download failed on URL, %s because of %s', self.download_data.url, str(e) )

    def extract_img_links(self):
        img_links = self.extractor.get_img_links()
        self.img_links = img_links
       
    def extract_title(self):
        title = self.extractor.get_title()
        self.title = title

    def __repr__ (self):
        return f"WebComic: {self.download_data.url}"
    
    def get_dir_path(self):
        """Every webcomic has its directory where images are saved"""
        pass
        



# things = jsonpickle.decode('[{"py/object": "__main__.WebComic", "url": "Awesome"}, {"py/object": "__main__.Thing", "url": "Wonderful"}]')

# for thing in things:
#     thing.download()
#     thing.parse_img_links()
#     if len(thing.img_links) == 1:
        #compare to thing.img
        #download img if it is different
        #save in a folder
        #continue
    # thing.parse_title()
    #check all the images and inspect the one that contains the title
    #get that img link if found
    #else check img_link with the biggest size

    #compare thing.img_link to the one coming from the json
    #if different
    #ImageProcessor.process(thing.img_link) downloads the image, saves it in the correct folder, throws necessary error
    #if image processing is successful
    #update the object with the new image link i.e thing.set_img_link
    


# frozen = jsonpickle.encode(things)
#save frozen again
# print(frozen)



