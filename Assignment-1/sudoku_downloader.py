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
        self.sudoku = []
        self.difficulty = ''

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
                self.sudoku.append(str(int(data) - 1))
            except ValueError:
                self.sudoku.append('-1')
        elif self.div_open and not self.table_open:
            if data[:difficulty_prefix_len] == difficulty_prefix:
                self.difficulty = data[difficulty_prefix_len:data.index(' (')]


def parse():
    data = request.urlopen('http://www.menneske.no/sudoku/eng/random.html').read().decode('UTF-8')
    parser = PageParser()
    parser.feed(data)
    print(' '.join(parser.sudoku))
    print(parser.difficulty)


if __name__ == '__main__':
    for i in range(20000):
        parse()
