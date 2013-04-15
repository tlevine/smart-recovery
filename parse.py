#!/usr/bin/env python2
import string
import re
from collections import OrderedDict

from lxml.html import parse
from dumptruck import DumpTruck

def table():
    html = parse('showall.php')
    trs = html.xpath('//table/tr')
    header = map(unicode, trs.pop(0).xpath('td/descendant::text()'))
    for tr in trs:
        yield row(header, tr)

def row(header, tr):
    data = OrderedDict(zip(header, map(unicode, [td.text_content() for td in tr.xpath('td')])))
    data.update({
        'Email_Address': _email(tr),
        'Open_Meeting': _openness(tr),
        'Address': None,
        'Schedule': None,
        'Telephone': _telephone(tr.xpath('td[position()=4]')[0].text_content()),
    })
    return data

def main():
    dt = DumpTruck(dbname = '/tmp/smart.db')
    for data in table():
        dt.insert(data, 'smart', commit = False)
    dt.commit()

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

def _pm(time):
    hours, minutes = time.split(':')
    return unicode(int(hours) + 12) + ':' + minutes

def _schedule(meeting_location):
    'Returns (day, begin time, end time)'
    m = re.match(r'(?:.* )?([a-z]+day) ([0-9]{1,2}:[0-9]{2})[ -to]+([0-9]{1,2}:[0-9]{2}) ?([ap]m).*', meeting_location, flags = re.IGNORECASE)
    if not m:
        return (None, None, None)

    day = m.group(1)
    begin = m.group(2)
    end = m.group(3)

    day_half = m.group(4)
    if day_half.lower() == 'pm':
        begin = _pm(begin)
        end = _pm(end)

    return (day, begin, end)

def _telephone(raw):
    for group in re.split(r'(?:[a-zA-Z/]|   )', raw):
        phone = filter(lambda letter: letter in '1234567890', group)
        if len(phone) >= 10 and len(phone) <= 13:
            return phone

if __name__ == '__main__':
    main()
