import jsonpickle
from random import random
import network
import urls
import files
import logging
from enum import Enum


class WebComicDownloadStatus(Enum):
    NOT_STARTED = 0
    FAILED = 1
    SUCCESS = 2



class WebComicDownloaddata(object):
    def __init__(self, data):
        self.url = data ['url']
        self.latest_img_url = data['latest_img_url'] if 'latest_img_url' in data else ''
        self.last_tried = data['last_tried'] if 'latest_tried' in data else ''
        self.last_download_status = WebComicDownloadStatus.NOT_STARTED.name


class WebComic(object):
    def __init__(self):
        self._comic_html = ''
        self.extractor = None
        self.latest_img_content = ''
        self.page_download_status = WebComicDownloadStatus.NOT_STARTED.name
        self.download_data = None
     
    @property
    def comic_html(self):
        return self._comic_html
   
    @comic_html.setter
    def comic_html(self, comic_html):
        if comic_html:
            self._comic_html = comic_html
            self.page_download_status = WebComicDownloadStatus.SUCCESS.name
            logging.info('Page download successful for %s', self.download_data.url)
        else: 
            self.page_download_status = WebComicDownloadStatus.FAILED.name
            logging.debug('Html content is empty')


    def download_page(self):
        """Downloads the comic url's HTML content"""
        try:
            logging.info('Downloading page %s ....', self.download_data.url)
            html = network.download_html(self.download_data.url)
            self.comic_html = html
        except Exception as e:
            self.page_download_status = WebComicDownloadStatus.FAILED.name
            logging.debug('Download failed on URL, %s because of %s', self.download_data.url, str(e) )


    # Change to download all images that have that title, 
    # create a folder to store those images if they are more than one
    # look for a way to delete old image if a new one is present
    def download_latest_image(self):
        """Downloads latest image content """
        curr_img_url = self.extractor.extract_latest_img_url()
        if curr_img_url and curr_img_url != self.download_data.latest_img_url:
            try:
                logging.info('Downloading latest image for %s', self.download_data.url)   
                img_content = network.fetch_url(curr_img_url)[1]
                self.download_data.latest_img_url = curr_img_url
                self.latest_img_content = img_content
            except Exception as e:
                logging.debug('Exception while trying to download image %s because of %s', curr_img_url, str(e) )
        else:
            logging.debug('Not downloading current image for %s because there is no new image', self.download_data.url)


    def save_image(self):
        """Saves downloaded image content if any to a file"""
        if self.latest_img_content:
            try:
                logging.info('Saving latest image for %s', self.download_data.url) 
                img_file_path = urls.get_img_file_path(self.download_data.url, self.download_data.latest_img_url)
                files.save_image_to_file(self.latest_img_content, img_file_path)
                logging.debug('Image saved successfully to path %s', img_file_path)
                self.download_data.last_download_status = WebComicDownloadStatus.SUCCESS.name
            except Exception as e: 
                logging.debug('Exception occured while trying to save image to path %s because of %s', img_file_path, str(e))
                self.download_data.last_download_status = WebComicDownloadStatus.FAILED.name
        else:
            logging.debug('Cannot save image that has not been downloaded')
            self.download_data.last_download_status = WebComicDownloadStatus.FAILED.name
        

    def __repr__ (self):
        return f"WebComic: {self.download_data.url}"
    

    
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



