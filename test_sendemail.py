from plone_egos import *

def test_correct_email():
    assert(send_email("content", ["address"], "smtp.gmail.com", 587, "nbpyclasstest@gmail.com", "The tweet report", {}) == None)