from collections import deque

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from typing import Generator


def crawl_pages(start_url: str, skip_url_patterns: list[str], max_depth: int) -> Generator[str, None, None]:
    """ Returns list of URLs in the page of the given URL. """
    q = deque()
    q.append((start_url, max_depth))
    visited = set()

    while len(q) > 0:
        url, depth = q.popleft()

        if depth <= 0:
            continue

        if url in visited:
            continue

        for pattern in skip_url_patterns:
            if pattern in url:
                continue

        try:
            # Send an HTTP request to the URL
            response = requests.get(url)

            if response.status_code == 200:
                yield url
                visited.add(url)

                # Crawl links in the page.
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find and follow links to child pages
                link_elements = soup.find_all('a', href=True)

                for link in link_elements:
                    child_url = urljoin(url, link['href'])
                    q.append((child_url, depth - 1))
            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to retrieve the webpage. Error: {e}")
