import threading
from queue import Queue
from Crawler import Crawler
from domain_parser import *
from file_jobs import *

PROJECT_NAME = 'Pardus'
HOME_PAGE = 'https://pardus.org.tr'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()

Crawler(PROJECT_NAME,HOME_PAGE,DOMAIN_NAME)


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        url = queue.get()
        Crawler.crawl_page(threading.current_thread().name,url)
        queue.task_done()


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    crawled_links = file_to_set(CRAWLED_FILE)
    if (len(queued_links) > 0) and (queued_links != crawled_links):
        print(str(len(queued_links)) + " links in the queue.")
        create_jobs()

create_workers()
crawl()