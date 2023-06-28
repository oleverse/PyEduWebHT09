import json
import requests
from bs4 import BeautifulSoup

import author
import quote


class QuotesParser:
    def __init__(self, base_url):
        self.ready = False
        self.node = None
        self.base_url = base_url
        self.__authors = []
        self.__quotes = []

    def __get_ready(self, url, params=None):
        print(f'Processing URL: {url}')
        response = requests.get(url, params=params)

        if response.status_code == 200:
            self.node = BeautifulSoup(response.text, 'lxml')
            self.ready = self.node is not None
        else:
            print(f"Web server returned HTTP {response.status_code}")
            print(f"URL '{url}' is not accessible.")
            self.ready = False

    def __get_author(self, author_about_url):
        url = f'{self.base_url}{author_about_url}'
        self.__get_ready(url)

        if self.ready:
            return author.Author(
                born_date=self.node.select('span.author-born-date')[0].text.strip(),
                born_location=self.node.select('span.author-born-location')[0].text.strip(),
                description=self.node.select('div.author-description')[0].text.strip()
            )

    @staticmethod
    def __get_quote(author_name, quote_block):
        return quote.Quote(
            author=author_name,
            quote=quote_block.find('span', attrs={'class': 'text'}).text.strip(),
            tags=[a.text.strip() for a in quote_block.select('div.tags a.tag')]
        )

    @property
    def authors(self):
        print(f'Total authors count: {len(self.__authors)}')
        return json.dumps(self.__authors, ensure_ascii=False, indent=2)

    @property
    def quotes(self):
        print(f'Total quotes count: {len(self.__quotes)}')
        return json.dumps(self.__quotes, ensure_ascii=False, indent=2)

    def parse_data(self):
        page_url = self.base_url
        authors_dict, quotes_dict = {}, {}

        while True:
            self.__get_ready(page_url)
            if self.ready:
                authors_parsed = quotes_parsed = 0
                content = self.node
                for quote_block in content.select('div.quote'):
                    if author_block := quote_block.select('small.author'):
                        author_name = author_block[0].text.strip()
                        if author_name not in authors_dict:
                            author_about = author_block[0].find_next_sibling('a')
                            authors_dict[author_name] = self.__get_author(author_about["href"])
                            authors_dict[author_name]["fullname"] = author_name
                            authors_parsed += 1
                        self.__quotes.append(self.__get_quote(author_name, quote_block).data)
                        quotes_parsed += 1

                print(f'\tNew authors parsed: {authors_parsed}')
                print(f'\tQuotes parsed: {quotes_parsed}')

                if next_nav_anchors := content.select('nav ul.pager li.next a'):
                    page_url = f'{self.base_url}{next_nav_anchors[0]["href"]}'
                else:
                    break

        self.__authors = [a.data for a in authors_dict.values()]
