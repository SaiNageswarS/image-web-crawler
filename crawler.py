import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from data_items import ScrapeSiteItem


def crawl_pages(site: ScrapeSiteItem, visited: set[str]) -> list[str]:
    """ Returns list of URLs in the domain of the given URL. """
    url = site.src_url
    result = []

    if url in visited:
        return result

    if site.max_depth <= 0:
        return result

    for pattern in site.skip_url_patterns:
        if pattern in url:
            return result

    visited.add(url)

    print(f"Scraping {url}")

    try:
        # Send an HTTP request to the URL
        response = requests.get(url)

        if response.status_code == 200:
            result.append(url)

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
                result = result + child_items
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to retrieve the webpage. Error: {e}")

    return result
