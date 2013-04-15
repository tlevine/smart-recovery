import nose.tools as n
import parse

def _compare(function, raw_expected):
    for raw, expected in raw_expected:
        observed = parse._location(raw)
        n.assert_equal(observed, expected)

def test_address():
    _compare (parse._location, [
        (
            'Wednesday 5:00-6:30 PM     Providence Portland Medical Center    4805 NE Glisan    Enter through main doors on Glisan side.  Room HCC6',
            'Providence Portland Medical Center\n4805 NE Glisan'
        ),
        (
            'Wednesday 16:30-18:00    Henry Windsor House 13 Pitt Street S70 1AL',
            'Henry Windsor House\n13 Pitt Street\nS70 1AL'
        ),
        (
            'Thursday 6:30 PM        1700 S. 24th St.  (east entrance) ',
            '1700 S. 24th St.',
        ),
        (
            'Tuesday 11:30-13:00    Turning Point 44 Sidney Street S1 4RH',
            'Turning Point\n44 Sidney Street S1 4RH',
        ),
    ]

def test_schedule():
    _compare (parse._location, [
        (
            'Wednesday 5:00-6:30 PM     Providence Portland Medical Center    4805 NE Glisan    Enter through main doors on Glisan side.  Room HCC6',
            ('Wednesday', '5:00', '6:30')
        ),
        (
            'Wednesday 16:30-18:00    Henry Windsor House 13 Pitt Street S70 1AL',
            ('Wednesday', '16:30', '18:00')
        ),
        (
            'Thursday 6:30 PM        1700 S. 24th St.  (east entrance) ',
            ('Thursday', '18:30', None)
        ),
        (
            'Tuesday 11:30-13:00    Turning Point 44 Sidney Street S1 4RH',
            ('Tuesday', '11:30', '13:00')
        ),
    ]

def test_telephone():
    _compare (parse._location, [
        ('07814 129140', '07814129140'),
        ('447887677862', '447887677862'),
        ('07786 612561', '07786612561'),
        ('602-570-6179', '6025706179')
        ('+91-1744-291278      Cell number is : +91-94-164-10810', '911744291278')
        ('0131 220 3404/0131 225 6028', '01312203404'),
        ('920-495-0062           920-818-0062', '9204950062')
    ]
