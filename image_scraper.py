import argparse
import os
import urllib.request
import time
import yaml
import json
from selenium import webdriver

import socket
socket.setdefaulttimeout(10) #A timeout to exit while downloading the images using urllib.request if the request takes long time.

class ChromeScrapeImages:
    def __init__(self, search_text, folder_name, download_original_images=True, num_images=100):
        self.search_text = search_text
        self.download_original_images = download_original_images
        self.search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
        self.search_url = self.search_url.format(q=search_text)
        self.num_images = num_images
        self.folder = folder_name
        self.driver = webdriver.Chrome(executable_path='chromedriver/chromedriver')
    
    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

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
                    time.sleep(5)
                except Exception as e:
                    print ("Less images found: {}".format(e))
                    break

        if self.download_original_images:
            self.r = self.driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
        else:
            self.r = self.driver.find_elements_by_tag_name('img')

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        for idx, v in enumerate(self.r):
            img_info_inner_html = v.get_attribute('innerHTML')
            src =  json.loads(img_info_inner_html)['ou'] if self.download_original_images else v.get_attribute("src")

            if src != None:
                destination_file = self.folder + '/' + self.search_text.replace(' ', '_') + '_' + str(idx)
                try:
                    self.g = urllib.request.urlretrieve(src, destination_file)
                except Exception as e:
                    print("Error downloading original image: {}".format(e))

                total_images += 1

if __name__ == "__main__":
    n_images = 800 # The google image search gives only maximum about 700 to 800 images
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--yaml_file_name', type=str, default='search_queries.yaml', help='YAML file containing search terms')
    arg_parser.add_argument('--download_original_images', type=str, default='true', help='Is original image required? if not will download the thumbnail images in google')
    opt = arg_parser.parse_args()

    yaml_file = opt.yaml_file_name

    if opt.download_original_images.lower in ['yes', 'true', 'y', '1']:
        download_original_images = True
    else:
        download_original_images = False
    

    print(opt)
    with open(yaml_file) as f:
        docs = yaml.load_all(f)

        for doc in docs:
            for folder_name, search_terms in doc.items():
                for search_term in search_terms:
                    scrapper = ChromeScrapeImages(search_term, folder_name, download_original_images=download_original_images, num_images=n_images)
                    scrapper.scrape_images()