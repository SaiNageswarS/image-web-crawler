import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from data_items import ScrapeSiteItem
from typing import Generator


def crawl_pages(site: ScrapeSiteItem, visited: set[str]) -> Generator[str, None, None]:
    """ Returns list of URLs in the domain of the given URL. """
    url = site.src_url

    if url in visited:
        yield

    if site.max_depth <= 0:
        yield

    for pattern in site.skip_url_patterns:
        if pattern in url:
            yield

    visited.add(url)

    try:
        # Send an HTTP request to the URL
        response = requests.get(url)

        if response.status_code == 200:
            print(f"Crawl:  {url}")
            yield url

            # Crawl links in the page.
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find and follow links to child pages
            link_elements = soup.find_all('a', href=True)

            for link in link_elements:
                child_url = urljoin(url, link['href'])
                child_scrape_item = ScrapeSiteItem(src_url=child_url,
                                                   skip_url_patterns=site.skip_url_patterns,
                                                   max_depth=site.max_depth - 1)
                child_items = crawl_pages(child_scrape_item, visited)
                for child_url in child_items:
                    yield child_url
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to retrieve the webpage. Error: {e}")
