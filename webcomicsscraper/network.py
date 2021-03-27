import requests,bs4, logging
import urls
from PIL import Image, ImageFile

chunk_size = 1024

def download_html(url):
    """
    Downloads html content for the given url
    """
    res = requests.get(url)
    html = bs4.BeautifulSoup(res.text, 'html.parser')
    res.raise_for_status()
    return html
    

# def download_image(img_url):
#     """
#     Downloads image for the given img url
#     """
#     res = requests.get(img_url)
#     res.raise_for_status()
#     return res.content


def fetch_url(url, dimension=False):
    nothing = None if dimension else (None, None)

    if not url or not url.startswith(('http://', 'https://')):
        return nothing
        
    response = None
    while True:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            # if we only need the dimension of the image, we may not
            # need to download the entire thing
            content = response.raw.read(chunk_size) if dimension else response.content
            content_type = response.headers.get('Content-Type')

            if not content_type:
                return nothing

            if 'image' in content_type:
                p = ImageFile.Parser()
                new_data = content
                while not p.image and new_data:
                    try:
                        p.feed(new_data)
                    except IOError:       
                        p = None
                        break
                    except ValueError:
                        p = None
                        break
                    except Exception:
                        p = None
                        break
                    new_data = response.raw.read(chunk_size)
                    content += new_data

                if p is None:
                    return nothing
                # return the size, or return the data
                if dimension and p.image:
                    return p.image.size
                elif dimension:
                    return nothing
            elif dimension:
                # expected an image, but didn't get one
                return nothing
        
            return content_type, content
        finally:
            if response is not None:
                response.raw.close()
                if response.raw._connection:
                    response.raw._connection.close()    



# def fetch_url(url, dimension=False):
#     nothing = None if dimension else (None, None)

#     if not url.startswith(('http://', 'https://')):
#         return nothing

#     response = None
#     while True:
#         # try:
#         response = requests.get(url, stream=True)
#         # if we only need the dimension of the image, we may not
#         # need to download the entire thing
#         content = response.raw.read(chunk_size) if dimension else response.content
#         content_type = response.headers.get('Content-Type')
#         if not content_type:
#             return nothing

#         if 'image' in content_type:
#             p = ImageFile.Parser()
#             new_data = content
#             while not p.image and new_data:
#                 try:
#                     p.feed(new_data)
#                 except IOError:       
#                     p = None
#                     break
#                 except ValueError:
#                     p = None
#                     break
#                 except Exception:
#                     p = None
#                     break
#                 new_data = response.raw.read(chunk_size)
#                 content += new_data

#             if p is None:
#                 return nothing
#             # return the size, or return the data
#             if dimension and p.image:
#                 return p.image.size
#             elif dimension:
#                 return nothing
#         elif dimension:
#             # expected an image, but didn't get one
#             return nothing
#         response.raise_for_status()
#         return content_type, content

#         # except requests.exceptions.RequestException as e:
#         #         logging.debug('error while fetching: %s because of %s', url, e)
#         #         return nothing
#         # finally:
#         #     if response is not None:
#         #         response.raw.close()
#         #         if response.raw._connection:
#         #             response.raw._connection.close()                       