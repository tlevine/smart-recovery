#!/usr/bin/env python2
import string
import re
from collections import OrderedDict
from math import floor

import chomsky as c
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
    day, begin, end = _schedule(data['Meeting_Location'])
    data.update({
        'Email_Address': _email(tr),
        'Open_Meeting': _openness(tr),
        'Address': None,
        'Day': day,
        'Begin_Time': begin,
        'End_Time': end,
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

def _take_while(f, l):
    for i in l:
        if f(i):
            yield i
        else:
            break

def _address(meeting_location):
    'Returns an address or None'
    return '\n'.join(re.split(r'  +', meeting_location)[1:])

def _totime(rawtime):
    'Convert a raw time to a float'
    if rawtime != None:
        hours, minutes = map(float, re.split(r'[:.]', rawtime))
        return hours + (minutes / 60)

def _fromtime(time):
    'Convert a float time to unicode.'
    if time != None:
        hours = floor(time)
        minutes = 60 * (time - hours)
        return '%02d:%02d' % (hours, minutes)

def _apply_noonness(begin, end = None, noonness = None):
    'Given float times, apply noonness.'
    b = e = None
    if noonness != None:
        noonness = noonness.lower()

    if end == None:
        # If end is not specified
        if noonness == 'pm' and begin < 12:
            b = begin + 12
        elif begin < 7:
            # Early morning or afternoon?
            b = begin + 12
        else:
            # Otherwise
            b = begin
    else:
        # If end is specified
        if begin > end:
            b = begin
            end = end + 12
        elif noonness == 'pm' and begin < 12 and end < 12:
            b = begin + 12
            e = end + 12
        else:
            b = begin
            e = end
    return b, e

DAYS_OF_WEEK = {
    'Sunday ': 'Sunday',
    'Monday ': 'Monday',
    'Tuesday ': 'Tuesday',
    'Wednesday ': 'Wednesday',
    'Thursday ': 'Thursday',
    'Friday ': 'Friday',
    'Saturday ': 'Saturday',
    'Sun ': 'Sunday',
    'Mon ': 'Monday',
    'Tue ': 'Tuesday',
    'Wed ': 'Wednesday',
    'Thu ': 'Thursday',
    'Fri ': 'Friday',
    'Sat ': 'Saturday',
}
# https://pypi.python.org/pypi/chomsky/v0.0.8
def _schedule(meeting_location):
    'Returns (day, begin time, end time)'
    day_matcher = c.Any(*map(c.Literal, DAYS_OF_WEEK.keys()))
    matcher = day_matcher + \
        c.Regex('([0-9]{1,2}[.:][0-9]{2})', group = 1) + \
        c.Optional(c.Regex('[ -]+([0-9]{1,2}[.:][0-9]{2}) ?', group = 1)) + \
        c.Optional(c.Regex('([APap][Mm])')) + \
        c.Chars()

    day_raw,begin_raw,maybe_end_raw,maybe_noon,_ = matcher(meeting_location)
    day = DAYS_OF_WEEK[day_raw]
    begin = _totime(begin_raw)
    end = _totime(unicode(maybe_end_raw[0])) if len(maybe_end_raw) == 1 else None
    noon = unicode(maybe_noon[0]) if len(maybe_noon) == 1 else None

    # Clean up day, begin, end
    return tuple([unicode(day)] + map(_fromtime, _apply_noonness(begin, end, noon)))

def _telephone(raw):
    for group in re.split(r'(?:[a-zA-Z/]|   )', raw):
        phone = filter(lambda letter: letter in '1234567890', group)
        if len(phone) >= 10 and len(phone) <= 13:
            return phone

if __name__ == '__main__':
    main()
