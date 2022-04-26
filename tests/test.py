import sys

sys.path.insert(0, './src/')

from calendar_source_canvas import Canvas
from calendar_source_cbtf import Cbtf
from calendar_source_moodle import Moodle

def test_canvas_read():
    canvas_source = Canvas("", True, "./tests/individual-tests/canvas.txt")
    s = canvas_source.request()[0]
    ans = {'name': '18 Pipeline Cycle Counting Review Session ', 'type': 'Needs to be manually sorted', 'course': 'cs 233',
        'source_name': 'canvas', 'end timestamp': '2022/03/28/12/00', 'start date': '3/28/2022', 'end date': '3/28/2022',
        'start date and time': '08:00AM Monday, 28. March', 'end date and time': '12:00PM Monday, 28. March'}
    assert s == ans, "testing reading from canvas format"


def test_cbtf_read():
    cbtf_source = Cbtf("", True, "./tests/individual-tests/cbtf.txt")
    s = cbtf_source.request()[0]
    ans = {'name': 'CS 233 Quiz 1 LOCATION:057 Grainger Library', 'type': 'Exam/Quiz', 'course': 'CS 233', 'source_name': 'cbtf',
        'end timestamp': '2022/01/26/16/50', 'start date': '1/26/2022', 'end date': '1/26/2022',
        'start date and time': '04:00PM Wednesday, 26. January', 'end date and time': '04:50PM Wednesday, 26. January'}
    assert s == ans, "testing reading from cbtf format"

def test_moodle_read():
    moodle_source = Moodle("", True, "./tests/individual-tests/moodle.txt")
    s = moodle_source.request()[0]
    ans = {'name': 'Checkpoint Quiz - Module 41 closes', 'type': 'Needs to be manually sorted', 'course': 'MATH 257', 
    'source_name': 'moodle', 'end timestamp': '2022/04/21/23/59', 'start date': '4/21/2022', 'end date': '4/21/2022', 
    'start date and time': '11:59PM Thursday, 21. April', 'end date and time': '11:59PM Thursday, 21. April'}
    assert s == ans, "testing reading from moodle format"
