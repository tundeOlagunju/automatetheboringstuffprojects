import re

class ContentExtractor(object):
    def __init__(self, doc):
        self.doc = doc

    def extract_latest_img_url(self):
        if not self.doc:
            return None

        img_tags = self.extract_img_tags()
        if not img_tags:
            return None

        # return early if there is only one imag tag on the page
        if len(img_tags) == 1:
            return self.get_img_url_from_tag(img_tags[0]) 
        
        title = self.extract_title()
        img_tag_with_title = self.get_img_tag_with_title(img_tags, title)
        
        return self.get_img_url_from_tag(img_tag_with_title)
        
        
    def get_img_url_from_tag(self, img_tag):
        return img_tag.get('src') if img_tag and img_tag.get('src') else None

    
    def get_img_tag_with_title(self, img_tags, title):
        """ Inspect the img_tags' atrributes alt and title and src returns the first tag which contains the title """

        def get_img_tag(attr, tag, title):
            title = title.strip().lower()
            if tag and tag.get(attr):
                attr_val = tag.get(attr).strip().lower()
                return tag if title in attr_val or attr_val in title else None

        try_alt , try_title, try_src = [None]*3
        for tag in img_tags:
            try_title = get_img_tag('title', tag, title)
            if not try_title:
                try_alt = get_img_tag('alt', tag, title)
                if not try_alt:
                    try_src = get_img_tag('src', tag, title)
            if try_alt or try_title or try_src:
                return try_title or try_alt or try_src
    

    def extract_img_tags(self):
        """ Extracts all image src links from the html document """
        if self.doc:
            img_tags = self.doc.find_all('img')
            return img_tags
            # return [img_tag.get('src') for img_tag in img_tags if img_tag.get('src')]


    def extract_title(self):
        """Extracts the relevant title from the page by trying different techniques
        Assumptions:
        1. Extract title from the <h1> <h2> or <h3> tags with *title as class. More specifically, from <h2> <a> href </a> </h2>
         Most comic websites have title in their <h2>, therefore it will be tried first
        2. Extract title from the <title> tag or og:: title in the head. As urls in the input file are base urls, this title in most 
        cases are the page urls, rather than the comic urls. If step 1 fails to find a title, the title in the head is most likely the 
        title of the comic url
        """

        try_h2, try_h1, try_h3, try_head = [None] * 4
        
        try_h2 = self.extract_title_from_h_tag('h2')
        if not try_h2:
            try_h1 = self.extract_title_from_h_tag('h1')
            if not try_h1:
                try_h3 = self.extract_title_from_h_tag('h3')
                if not try_h3:
                    try_head = self.extract_title_from_head()
        
        title = try_h1 or try_h2 or try_h3 or try_head
        return title


    def extract_title_from_h_tag(self, h_tag):
        """Assumptions (in order of accuracy)
        1. Checks the class attribute value of the h tags which contains 'title'
        2. For h tags without title, we get the text value of the a_tag in the first h_tag
        """
        regex = re.compile('.*title.*')
        for h_tag_with_title in self.doc.find_all(h_tag, {'class' : regex}):
            for a_tag in h_tag_with_title.find_all('a'):
                return a_tag.text
        
        for h_tag in self.doc.find_all(h_tag):
            for a_tag in h_tag.find_all('a'):
                return a_tag.text
        

    def extract_title_from_head(self):
        title_head, og_title = [None] * 2

        #first title from head title
        for title in self.doc.title.children:
            title_head = title
            break
        
        #title from og::title
        if not title_head:
            og_title = self.extract_meta_title('meta[property="og:title"]') or self.extract_meta_title('meta[name="og:title"]')

        return title_head or og_title

    def extract_meta_title(self, meta):
        return self.doc.select(meta)[0]['content']


        



        