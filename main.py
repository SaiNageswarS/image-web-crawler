from crawler import Crawler
from data_items import ScrapeSiteItem
from extract_images import extract_images
from index_image_text import vectorize_item


if __name__ == '__main__':
    index_items = [
        ScrapeSiteItem(
            src_url='https://economictimes.indiatimes.com/news/newsblogs/israel-palestine-war-live-news-gaza-strip-conflict-hamas-rocket-attack-jerusalem-operation-al-aqsa-flood-benjamin-netanyahu-latest-updates-day-6/liveblog/104355231.cms',
            skip_url_patterns=['coupons', 'subscribe', 'login', 'register', 'privacy', 'terms', 'contact',
                               'offers', 'newsletter', 'about', 'advertise', 'classifieds', 'careers',
                               'shop', 'games', 'ebooks', 'mobile', 'apps', 'food'],
            max_depth=1),

        ScrapeSiteItem(
            src_url='https://economictimes.indiatimes.com/',
            skip_url_patterns=['coupons', 'subscribe', 'login', 'register', 'privacy', 'terms', 'contact',
                               'offers', 'newsletter', 'about', 'advertise', 'classifieds', 'careers',
                               'shop', 'games', 'ebooks', 'mobile', 'apps', 'food'],
            max_depth=3),
    ]

    crawler = Crawler(set())
    for item in index_items:
        page_urls = crawler.crawl_pages(item)
        for page_url in page_urls:
            image_text = extract_images(page_url)

            if len(image_text) > 0:
                vectorize_item(image_text)
