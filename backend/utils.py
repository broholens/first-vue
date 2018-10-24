import string
import random
import hashlib

candidates = string.ascii_letters + string.digits

def create_salt(length=5):
    return ''.join(random.sample(candidates, length))
    
def add_salt(password, salt):
    md = hashlib.md5()
    new_pass = (password + salt).encode('utf-8')
    md.update(new_pass)
    return md.hexdigest()

def check_passwd(user, passwd):
    new_pass = (passwd + user.salt).encode('utf-8')
    md = hashlib.md5()
    md.update(new_pass)
    if md.hexdigest() == user.passwd:
        return True
    return False

def seconds_to_human_time(seconds):
    m, _ = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h == 0:
        return f'{m}分钟'
    return f'{h}小时{m}分钟'
