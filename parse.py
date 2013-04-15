#!/usr/bin/env python2
from csv import writer
from lxml.html import parse

def main():
    html = parse('showall.php')
    trs = html.xpath('//table/tr')
    header = clean_header(trs.pop(0))


def clean_header(tr):
    return tr.xpath('td/descendant::text()')
