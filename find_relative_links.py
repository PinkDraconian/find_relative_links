import re
import sys
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup


def extract_links(url):
    page = BeautifulSoup(requests.get(url).text, 'html.parser')
    relative_links = set()

    # Relative URLs can be found in style tags
    for style in page.findAll('style'):
        url_regex = r'url\(([\'"]?)(.*)\1\)'
        matches = re.findall(url_regex, style.text)
        [relative_links.add(match[1]) for match in matches]

    # Relative URLs can be found in a tags
    for a in page.findAll('a', attrs={'href': True}):
        if (
            len(a['href'].strip()) > 1
            and a['href'][0] != '#'
            and 'javascript:' not in a['href'].strip()
            and 'mailto:' not in a['href'].strip()
            and 'tel:' not in a['href'].strip()
        ):
            if 'http' in a['href'].strip() or 'https' in a['href'].strip():
                if urlparse(url).netloc.lower() in urlparse(a['href'].strip()).netloc.lower():
                    relative_links.add(a['href'])
            else:
                relative_links.add(a['href'])

    return relative_links


def main():
    url = sys.argv[1]
    links = extract_links(url)
    for link in links:
        print(urljoin(url, link))


if __name__ == '__main__':
    main()
