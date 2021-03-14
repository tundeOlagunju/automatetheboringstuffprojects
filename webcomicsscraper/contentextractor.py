import re

class ContentExtractor(object):
    def __init__(self, doc):
        self.doc = doc


    def extract_img_urls(self):
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
        regex = re.compile('.*title.*')
        for h_tag_with_title in self.doc.find_all(h_tag, {'class' : regex}):
            for a_tag in h_tag_with_title.find_all('a'):
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


        



        