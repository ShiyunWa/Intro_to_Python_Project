"""Test function for Class MyEmail."""

from classes import MyEmail

def test_class():
    """Test the Email class."""

    email_obj = MyEmail()

    # Test attributes
    assert email_obj.user_name == 'shiyunwa@gmail.com'
    assert email_obj.app_password == 'qedwovadjvqairbb'
    assert isinstance(email_obj.receivers, list)
    assert isinstance(email_obj.mail_content, str)

    # Test method user_check(self, input_string, choice='sender')
    assert callable(email_obj.user_check)
    assert email_obj.user_check('not_valid_email') == False
    assert email_obj.user_check('valid email@126.com') == False
    assert email_obj.user_check('shiyunwa@gmail.com') == True

    assert email_obj.user_check('Quit', 'receiver') == True
    assert email_obj.user_check('not_valid_email', 'receiver') == False
    assert email_obj.user_check('valid_email@qq.com', 'receiver') == True
    assert email_obj.user_check('walsonmail @ 163 . com', 'receiver') == True
