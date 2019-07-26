## Download google images - Python

### Dependencies:
1. Selenium

### Steps:
1. Download the chrome driver from [https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads). The correct version of chrome driver according to your google chrome version must be downloaded. More info on versions here: [https://stackoverflow.com/questions/41133391/which-chromedriver-version-is-compatible-with-which-chrome-browser-version/49618567#49618567](https://stackoverflow.com/questions/41133391/which-chromedriver-version-is-compatible-with-which-chrome-browser-version/49618567#49618567)

2. Create a directory `chromedriver`. Put the downloaded chromedriver executable inside it.

3. Modify `search_queries.yaml` file where you have to specify the folder name and the queries for your search.

3. Run `python image_scrapper.py` to download all the required images.

