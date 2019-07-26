import os
import urllib.request
import time
import yaml
from selenium import webdriver

class ChromeScrapeImages:
    def __init__(self, search_text, folder_name, num_images=100):
        self.search_text = search_text
        self.search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
        self.search_url = self.search_url.format(q=search_text)
        self.num_images = num_images
        self.folder = folder_name
        self.driver = webdriver.Chrome(executable_path='chromedriver/chromedriver')
    
    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def scrape_images(self):
        self.driver.get(self.search_url)
        total_images = 0
        while(total_images < self.num_images):
            images_meta = self.driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
            if len(images_meta) > total_images:
                total_images = len(images_meta)
                self.scroll_to_bottom()
            else:
                try:
                    self.driver.find_element_by_id('smb').click()
                    time.sleep(2)
                except Exception as e:
                    print ("Less images found: {}".format(e))
                    break

        self.r=self.driver.find_elements_by_tag_name('img')

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        for idx, v in enumerate(self.r):
            src = v.get_attribute("src")
            if src != None:
                destination_file = self.folder + '/' + self.search_text.replace(' ', '_') + '_' + str(idx)
                self.g = urllib.request.urlretrieve(src, destination_file)
                total_images += 1

if __name__ == "__main__":
    n_images = 800 # The google image search gives only maximum about 700 to 800 images
    
    with open('search_queries.yaml') as f:
        docs = yaml.load_all(f)

        for doc in docs:
            for folder_name, search_terms in doc.items():
                for search_term in search_terms:
                    scrapper = ChromeScrapeImages(search_term, folder_name, n_images)
                    scrapper.scrape_images()