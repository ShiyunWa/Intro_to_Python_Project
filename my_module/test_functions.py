"""Test functions for three fundamental functions."""

import functions

def test_boundary():
    """Test send_email(offset_num, direction = 'right')."""

    assert callable(functions.send_email)

def test_encode():
    """Test encode_email(input_string, offset_num, direction = 'right')."""

    assert callable(functions.encode_email)
    assert isinstance('XYZxyzABCDabcd 123456!@#$', str)
    assert functions.encode_email('XYZxyzABCDabcd 123456!@#$', 1) == 'YZAyzaBCDEbcde!234567"A$%'
    assert functions.encode_email('XYZxyzABCDabcd 123456!@#$', 1, 'left') == 'WXYwxyZABCzabc012345 ?"#'

def test_decode():
    """Test decode_email(input_string, offset_num, direction = 'left')."""

    # Notice: since I used the input() in the decode_email() function,
    # if directly use pytest to test this test function will fail.
    # To avoid such a situation, the appropriate pytest syntax should be:
    # pytest test_functions.py --capture=no
    # I found the source from https://blog.csdn.net/li_rshan/article/details/107082625

    assert callable(functions.decode_email)
    assert isinstance('vjku"ku"vjg"ockp"dqfa0ZABcde', str)
    assert functions.decode_email('vjku"ku"vjg"ockp"dqfa0ZABcde', 1) == 'uijt!jt!uif!nbjo!cpez/YZAbcd'
    assert functions.decode_email('vjku"ku"vjg"ockp"dqfa0ZABcde', 2) == 'this is the main body.XYZabc'
