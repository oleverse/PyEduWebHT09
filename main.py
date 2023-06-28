import os
import pathlib

from parser import QuotesParser


def main():
    parser = QuotesParser('http://quotes.toscrape.com')
    parser.parse_data()

    os.makedirs(pathlib.Path('data'), exist_ok=True)

    with open(file_name := pathlib.Path('data/authors.json'), 'w') as authors_fh:
        authors_fh.write(parser.authors)
    print(file_name, 'has been written.')

    with open(file_name := pathlib.Path('data/quotes.json'), 'w') as quotes_fh:
        quotes_fh.write(parser.quotes)
    print(file_name, 'has been written.')


if __name__ == "__main__":
    main()
