#!/usr/bin/env python2
from lxml.html import parse

def table():
    html = parse('showall.php')
    trs = html.xpath('//table/tr')
    header = unicode(trs.pop(0).xpath('td/descendant::text()'))
    for tr in trs:
        yield row(header, tr)

def row(header, tr):
    data = zip(header, map(unicode, [td.text_content() for td in tr.xpath('td')]))


def _email(tr):
    pass

def _openness(tr):
    'Returns True, False or None'
    pass

def _location(meeting_location):
    'Returns an address or None'
    pass

def _schedule(meeting_location):
    'Returns (day, begin time, end time)'
    pass

def _telephone(raw):
    pass

