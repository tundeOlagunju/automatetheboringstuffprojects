import tldextract, os, files, re

#parse domain manually 
# prep img url

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

def prepare_img_url(img_url, url):
    if not url:
        return None
    img_url = remove_leading_slashes(img_url)
    url = remove_trailing_slashes(url)
    domain = get_domain_from_url(url)
    if domain in img_url:
        return 'http://' + img_url
    return url + '/' + img_url

def clean_img_file_name(file_name):
    """
    Cleans image file name. Turns gdgdggdgd.png?sgsgsgjdueydnnd into gdgdggdgd.png. Does nothing 
    if the image file name is already clean
    """

    #get the file extension and remove all characters after that
    ext_regex = re.compile(r'(jpg|png|gif)')
    ext = ext_regex.search(file_name).group()
    cleaned_name = file_name.split(ext)[0] + ext
    return cleaned_name


def get_file_name (img_url):
    # last part of the image url
    base_name = os.path.basename(img_url)
    file_name = clean_img_file_name(base_name)
    return file_name
    
def get_img_file_path(url, img_url):
    domain = get_domain_from_url(url)
    img_dir = files.join_path('bin', domain)
    files.make_dir(img_dir)

    file_name = get_file_name(img_url)
    file_path = files.join_path(img_dir, file_name)
    return file_path
