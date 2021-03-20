import tldextract, os, files

#parse domain manually 
# prep img url

def get_domain_from_url(url):
    ext = tldextract.extract(url)
    return ext.domain

def prepare_img_url(url):
    if url is None:
        return None
    if url.startswith(('http', 'https')):
        return url
    return 'http:' + url
    

def get_img_file_path(url, img_url):
    domain = get_domain_from_url(url)
    img_dir = files.join_path('bin', domain)
    files.make_dir(img_dir)
    # last part of the image url
    img_name = os.path.basename(img_url)
    img_file_path = files.join_path(img_dir, img_name)
    return img_file_path
