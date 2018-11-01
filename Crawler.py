from link_finder import LinkFinder
from file_jobs import *
from domain_parser import *
from urllib.request import urlopen


class Crawler():

    project_Name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Crawler.project_Name = project_name
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.queue_file = Crawler.project_Name + '/queue.txt'
        Crawler.crawled_file = Crawler.project_Name + '/crawled.txt'

        self.boot()
        self.crawl_page("First thread", Crawler.base_url)

    @staticmethod
    def boot():
        directory_create(Crawler.project_Name)
        create_data_files(Crawler.project_Name,Crawler.base_url)
        Crawler.queue = file_to_set(Crawler.queue_file)
        Crawler.crawled = file_to_set(Crawler.crawled_file)

    @staticmethod
    def crawl_page(thread_name , page_url):
        if page_url not in Crawler.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue  ' + str(len(Crawler.queue)) + '| Crawled  ' + str(len(Crawler.crawled)))
            Crawler.add_links_to_queue(Crawler.gather_links(page_url))
            Crawler.crawled.add(page_url)
            Crawler.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                htmL_bytes = response.read()
                html_string = htmL_bytes.decode('utf-8')
            finder = LinkFinder(Crawler.base_url,page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()

        return finder.get_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Crawler.queue) or (url in Crawler.crawled):
                continue
            if Crawler.domain_name != get_domain_name(url):
                continue
            Crawler.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Crawler.queue,Crawler.queue_file)
        set_to_file(Crawler.crawled,Crawler.crawled_file)