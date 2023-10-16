from crawler import crawl_pages
from extract_images import extract_images
from index_image_text import vectorize_item


if __name__ == '__main__':
    src_url: str = 'https://economictimes.indiatimes.com/'
    skip_url_patterns = ['coupons', 'subscribe', 'login', 'register', 'privacy', 'terms', 'contact',
                         'offers', 'newsletter', 'about', 'advertise', 'classifieds', 'careers',
                         'shop', 'games', 'ebooks', 'mobile', 'apps', 'food']

    for page_url in crawl_pages(src_url, skip_url_patterns, 5):
        image_text = extract_images(page_url)

        if len(image_text) > 0:
            vectorize_item(image_text)

