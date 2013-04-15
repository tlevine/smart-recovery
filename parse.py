#!/usr/bin/env python2
import re
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
    cells = [td.text_content() for td in tr.xpath('td')]
    for cell in cells:
        m = re.match(r'(?:.* )?([^ ]+)(?:"AT"|\@)([^ ]+).*', cell)
        if m:
            return m.group(1) + '@' + m.group(2)

def _openness(tr):
    'Returns True, False or None'
    lowercased = tr.text_content().lower()
    if 'closed group' in lowercased or 'closed meeting' in lowercased:
        return False
    elif 'open group' in lowercased or 'open meeting' in lowercased:
        return True
    else:
        return None

def _address(meeting_location):
    'Returns an address or None'
    pass

def _schedule(meeting_location):
    'Returns (day, begin time, end time)'
    pass

import string
def _telephone(raw):
    for group in re.split(r'(?:[a-zA-Z/]|   )', raw):
        phone = filter(lambda letter: letter in '1234567890', group)
        if len(phone) >= 10 and len(phone) <= 13:
            return phone

