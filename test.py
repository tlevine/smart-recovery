from lxml.html import fromstring
import nose.tools as n
import parse

def _compare(function, raw_expected):
    for raw, expected in raw_expected:
        observed = function(raw)
        n.assert_equal(observed, expected)

def test_address():
    _compare(parse._address, [
        (
            'Wed 10.30 - 12.00pm Access Community Group, Warilla Scout Hall Lowe Park George Street',
            'Warilla Scout Hall\nLowe Park\nGeorge Street'
        ),
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
    ])

def test_schedule():
    _compare(parse._schedule, [
        (
            'Wed 10.30 - 12.00pm Access Community Group, Warilla Scout Hall Lowe Park George Street',
            'Wednesday', '10:30', '12:00'
        ),
        (
            'Wednesday 5:00-6:30 PM     Providence Portland Medical Center    4805 NE Glisan    Enter through main doors on Glisan side.  Room HCC6',
            ('Wednesday', '17:00', '18:30')
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
    ])


def test_telephone():
    _compare(parse._telephone, [
        ('07814 129140', '07814129140'),
        ('447887677862', '447887677862'),
        ('07786 612561', '07786612561'),
        ('602-570-6179', '6025706179'),
        ('+91-1744-291278      Cell number is : +91-94-164-10810', '911744291278'),
        ('0131 220 3404/0131 225 6028', '01312203404'),
        ('920-495-0062           920-818-0062', '9204950062')
    ])

def test_openness():
    _compare(parse._openness, [
        (
            fromstring('<tr><td bgcolor="#FFFFFF" width="10%"><font size="2">Australia</font></td>\n <td bgcolor="#FFFFFF" width="10%"><font size="2">QLD</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">Kirra</font></td>\n <td bgcolor="#FFFFFF" width="20%"><font size="2">ON HOLD ,Kirra Hill Community Centre, Powell/Garrick St</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2"></font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">Jane Su-Ming Lai</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2"></font></td>\n</tr>'),
            None
        ),
        (
            fromstring('<tr><td bgcolor="#F0F0F0" width="10%"><font size="2">USA</font></td>\n <td bgcolor="#F0F0F0" width="10%"><font size="2">Wisconsin</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">Madison (CLOSED MEETING, FOR PATIENTS ONLY)</font></td>\n <td bgcolor="#F0F0F0" width="20%"><font size="2">Thursday    2:30-3:15  Mendota Mental Health Institution (MMHI)</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">608-301-1487</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">Bruce Christianson (F)</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">Bruce.Christianson"AT"dhs.wisconsin.gov</font></td>\n</tr>'),
            False
        )
    ])

def test_email():
    _compare(parse._email, [
        (
            fromstring('<tr><td bgcolor="#FFFFFF" width="10%"><font size="2">United Kingdom</font></td>\n <td bgcolor="#FFFFFF" width="10%"><font size="2"></font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">London (Greater)</font></td>\n <td bgcolor="#FFFFFF" width="20%"><font size="2">Sunday 12:00-13:30    19 Tudor Road Hackney E9 7SN</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2"></font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">Thomas Baillie (F)</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">t.bailie50"AT"gmail.com  07918 747 277</font></td>\n</tr>'),
            't.bailie50@gmail.com'
        ),
        (
            fromstring('<tr><td bgcolor="#F0F0F0" width="10%"><font size="2">Australia</font></td>\n <td bgcolor="#F0F0F0" width="10%"><font size="2">NSW</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">Lismore</font></td>\n <td bgcolor="#F0F0F0" width="20%"><font size="2">Thurs 5.00 - 6.30pm, Riverlands Drug &amp; Alcohol Centre  (Meeting Room), Cnr Uralba &amp; Hunter Sts </font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">0459 848 043</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">laine Rees</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2"></font></td>\n</tr>'),
            None
        ),
        (
            fromstring('<tr><td bgcolor="#FFFFFF" width="10%"><font size="2">USA</font></td>\n <td bgcolor="#FFFFFF" width="10%"><font size="2">Ohio</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">Cincinnati Area (also listed under Greendale, IN)</font></td>\n <td bgcolor="#FFFFFF" width="20%"><font size="2">GREENDALE, IN    Monday 6:00 PM    Emanual Lutheran Church    570 Sheldon St.</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">859-282-6044        859-409-8997</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">Ken Witt (F)</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">yitzak"AT"insightbb.com</font></td>\n</tr>'),
            'yitzak@insightbb.com'
        ),
        (
            fromstring('<tr><td bgcolor="#FFFFFF" width="10%"><font size="2">Australia</font></td>\n <td bgcolor="#FFFFFF" width="10%"><font size="2">QLD</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">Kirra</font></td>\n <td bgcolor="#FFFFFF" width="20%"><font size="2">ON HOLD ,Kirra Hill Community Centre, Powell/Garrick St</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2"></font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2">Jane Su-Ming Lai</font></td>\n <td bgcolor="#FFFFFF" width="15%"><font size="2"></font></td>\n</tr>'),
            None
        ),
        (
            fromstring('<tr><td bgcolor="#F0F0F0" width="10%"><font size="2">USA</font></td>\n <td bgcolor="#F0F0F0" width="10%"><font size="2">Wisconsin</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">Madison (CLOSED MEETING, FOR PATIENTS ONLY)</font></td>\n <td bgcolor="#F0F0F0" width="20%"><font size="2">Thursday    2:30-3:15  Mendota Mental Health Institution (MMHI)</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">608-301-1487</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">Bruce Christianson (F)</font></td>\n <td bgcolor="#F0F0F0" width="15%"><font size="2">Bruce.Christianson"AT"dhs.wisconsin.gov</font></td>\n</tr>'),
            'Bruce.Christianson@dhs.wisconsin.gov'
        )
    ])
