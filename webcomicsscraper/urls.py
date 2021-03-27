import tldextract, os,  re
import files

#parse domain manually 
# prep img url

def refine_img_url(img_url, url):
    prep_img_url = prepare_img_url(img_url, url)
    cleaned_img_url  = clean_img_file_url(prep_img_url) #clean the end part of the url 
    return cleaned_img_url

def prepare_img_url(img_url, url):
    if not url or not img_url:
        return None
    if img_url.startswith(('https://', 'http://')):  #No need to prepare the url if starts with http or https
        return img_url
    img_url = remove_leading_slashes(img_url)
    url = remove_trailing_slashes(url)
    domain = get_domain_from_url(url)
    if domain in img_url:
        return 'http://' + img_url
    return url + '/' + img_url


def get_domain_from_url(url):
    if not url:
        return None
    ext = tldextract.extract(url.strip())
    return ext.domain


def remove_leading_slashes(url):
    if not url:
        return None
    return url.strip('//')


def remove_trailing_slashes(url):
    if not url:
        return None
    if url.endswith('/'):
        url = url[:-1]
    return url

def clean_img_file_url(img_url):
    """
    Cleans image file name. Refines https://hdhd.com/gdgdggdgd.png?sgsgsgjdueydnnd to https://hdhd.com/gdgdggdgd.png.
     Does nothing if the image file name is already clean
    """
    if not img_url:
        return None
    #get the file extension and remove all characters after that
    ext_regex = re.compile(r'(jpg|png|gif)')
    ext_group = ext_regex.search(img_url)

    if not ext_group:
        return None
    
    ext = ext_group.group()
    cleaned_url = img_url.split(ext)[0] + ext
    return cleaned_url

def get_img_file_path(url, img_url):
    domain = get_domain_from_url(url)
    img_dir = files.join_path('bin', domain)
    files.make_dir(img_dir)

    file_name = files.get_base_name(img_url)
    file_path = files.join_path(img_dir, file_name)
    return file_path




