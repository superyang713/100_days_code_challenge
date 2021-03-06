import re
import requests
from bs4 import BeautifulSoup
from content import Content
import logbook


crawler_log = logbook.Logger('Crawler')


class Crawler:
    def __init__(self, site):
        """
        The website object is a property of the Crawler object itself. This is
        to store the visited pages in the crawler. Whether to make a crawler
        website-agnostic or to make the website an attribute of the crawler is
        a design decision for the specific needs.
        """
        self.site = site
        self.visited = []

    def get_page(self, url):
        try:
            crawler_log.trace('Starting to request the webpage from {}'
                              .format(url))
            r = requests.get(url)
            crawler_log.trace('Request finished, status code {}'
                              .format(r.status_code))
        except requests.exceptions.RequestException as e:
            crawler_log.warn('Exceptions occured! Error message: {}'
                             .format(e))
            return None
        return BeautifulSoup(r.text, 'html.parser')

    def safe_get(self, page_obj, selector):
        """
        Untility function used to get a content string from a BeautifulSoup
        object and a selector. Returns an empty string if no object is found
        for the given selector
        """
        selected_elements = page_obj.select(selector)
        if selected_elements is not None and len(selected_elements) > 0:
            crawler_log.trace('Content found using selector {}'
                              .format(selector))
            return '\n'.join(
                [elem.get_text() for elem in selected_elements])
        return ''

    def parse(self, url):
        """
        Extract content from a given page URL
        """
        bs = self.get_page(url)
        if bs is not None:
            title = self.safe_get(bs, self.site.title_tag)
            body = self.safe_get(bs, self.site.body_tag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()
            else:
                crawler_log.warn('Article not found!')

    def crawl(self):
        """
        Get pages from website home page
        """
        bs = self.get_page(self.site.url)
        target_pages = bs.find_all(
            'a', href=re.compile(self.site.target_pattern)
        )
        for i, target_page in enumerate(target_pages, 1):
            crawler_log.trace('Starting to parse article {}'.format(i))
            target_page = target_page.attrs['href']
            if target_page not in self.visited:
                self.visited.append(target_page)
                if not self.site.absolute_url:
                    target_page = '{}{}'.format(self.site.url, target_page)
                self.parse(target_page)
            else:
                crawler_log.trace('Duplicated article!')
