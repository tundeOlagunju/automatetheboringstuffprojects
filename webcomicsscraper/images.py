import logging
import requests
from PIL import Image, ImageFile
import network

chunk_size = 1024

def largest_img_url(img_urls):
    max_area = 0
    max_url = None
    for img_url in img_urls:
        dimension = network.fetch_url(img_url, dimension=True)
        area = calculate_area(dimension)
        if area > max_area:
            max_area = area
            max_url = img_url
    logging.debug('using max img {}'.format(max_url))
    return max_url
    

def calculate_area(dimension):
    if not dimension:
        return 0
    area = dimension[0] * dimension[1]
    return area
    

