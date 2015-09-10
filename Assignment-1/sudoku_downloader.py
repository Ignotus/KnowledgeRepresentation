#!/usr/bin/env python3

from urllib import request
from html.parser import HTMLParser

difficulty_prefix = 'Difficulty: '
difficulty_prefix_len = len(difficulty_prefix)

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.div_open = False
        self.table_open = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            attributes = dict(attrs)
            if 'class' in attributes and attributes['class'] == 'grid':
                self.div_open = True
        elif tag == 'table':
            self.table_open = True

    def handle_endtag(self, tag):
        if tag == 'div':
            self.div_open = False
        elif tag == 'table':
            self.table_open = False

    def handle_data(self, data):
        if self.div_open and self.table_open and data != '\n':
            try:
                print(int(data) - 1, end=' ')
            except ValueError:
                print(-1, end=' ')
        elif self.div_open and not self.table_open:
            if data[:difficulty_prefix_len] == difficulty_prefix:
                print('\n' + data[difficulty_prefix_len:])

def parse():
    data = request.urlopen('http://www.menneske.no/sudoku/eng/random.html').read().decode('UTF-8')
    parser = PageParser()
    parser.feed(data)


if __name__ == '__main__':
    for i in range(1000):
        parse()
