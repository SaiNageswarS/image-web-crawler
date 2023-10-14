from celery import Celery

from crawler import crawl_pages
from data_items import ScrapeSiteItem
from extract_images import extract_images

app = Celery('SemanticImageSearchIngestion', broker='pyamqp://guest@localhost//')


@app.task
def crawl():
    index_items = [
        ScrapeSiteItem(
            src_url='https://www.thehindu.com/news/international/israel-hamas-conflict-live-updates-day-8/article67419467.ece',
            skip_url_patterns=['coupons', 'subscribe', 'login', 'register', 'privacy', 'terms', 'contact',
                               'offers', 'newsletter', 'about', 'advertise', 'classifieds', 'careers',
                               'shop', 'games', 'ebooks', 'mobile', 'apps', 'food'],
            max_depth=1),
    ]

    result = []
    for item in index_items:
        image_and_text = crawl_pages(item, set())
        print(image_and_text)
        result = result + image_and_text

    return result


@app.task
def extract_images_task(urls: list[str]):
    result = []

    for url in urls:
        image_text = extract_images(url)
        result = result + image_text

    return result


if __name__ == '__main__':
    app.start()
