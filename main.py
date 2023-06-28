import os
import pathlib

from parser import QuotesParser


def main():
    parser = QuotesParser('http://quotes.toscrape.com')
    parser.parse_data()

    os.makedirs(pathlib.Path('data'), exist_ok=True)

    with open(pathlib.Path('data/authors.json'), 'w') as authors_fh:
        authors_fh.write(parser.authors)

    with open(pathlib.Path('data/quotes.json'), 'w') as quotes_fh:
        quotes_fh.write(parser.quotes)


if __name__ == "__main__":
    main()
