from data_items import VectorDataItem
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# skip images which are icons, spacers, etc.
skip_image_pattern = ['logo', 'icon', 'spacer', 'pixel', 'blank', 'arrow', 'button', 'banner', 'ad',
                      'pixel', 'gif', 'svg']


def extract_images(url: str) -> list[VectorDataItem]:
    """ Returns list of images and their relevant text. """
    result = []

    try:
        # Send an HTTP request to the URL
        response = requests.get(url)

        if response.status_code == 200:
            # Crawl links in the page.
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find and follow links to child pages
            image_elements = soup.find_all('img', src=True)

            for image in image_elements:
                # check image width and height are greater than 100px if the attribute exists
                if 'width' in image and int(image['width']) < 100:
                    continue

                if 'height' in image and int(image['height']) < 100:
                    continue

                # skip images which are icons, spacers, etc.
                if __is_skip_image__(image):
                    continue

                image_url = urljoin(url, image['src'])

                # get text near the image - para, heading, etc.
                relevant_text = __normalize_text__(image.parent.text) + \
                                " " + \
                                __normalize_text__(image['alt'])

                # get text near the image - para, heading, etc.
                current_element = image

                while current_element:
                    if current_element.name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'):
                        relevant_text += " " + current_element.get_text()
                        break
                    current_element = current_element.find_previous()

                if len(relevant_text) < 50:
                    continue

                image_text_item = VectorDataItem(image_url=image_url,
                                                 relevant_text=relevant_text)
                print(f"Extract: {image_text_item}")
                result.append(image_text_item)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to retrieve the webpage. Error: {e}")

    return result


def __is_skip_image__(image: dict) -> bool:
    """ Returns True if the image is an icon, spacer, etc. """
    for pattern in skip_image_pattern:
        if pattern in image['src']:
            return True

    return False


def __normalize_text__(text: str) -> str:
    """ Returns normalized text. """
    text = text.lower().strip()
    # keep characters and replace everything else with space
    text = ''.join([c if c.isalpha() else ' ' for c in text])
    return text


if __name__ == '__main__':
    image_text = extract_images(
        'https://www.thehindu.com/news/international/israel-hamas-conflict-live-updates-day-8/article67419467.ece')
    for x in image_text:
        print(x)
