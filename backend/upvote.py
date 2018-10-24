import logging
import requests
# import grequests
from threading import Thread


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%d %b %Y %H:%M:%S',
)
logger = logging.getLogger('')


def get_proxy():
    try:
        proxy = requests.get('http://39.107.86.245:5010/get').text
        return {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
    except:
        return None


def url_mapping(url):
    user = url.split('userId=')[-1].split('@')[0]
    return f'https://ppssp.xdf.cn/Mobile_Teacher_Home/like?u={user}%40xdf.cn&protocol=https%3A'

def get_upvoted(url):
    # url = url_mapping(url)
    while True:
        try:
            return requests.get(url, timeout=5).json()['Count']
        except:
            pass

def _upvote(url, total_num):
    # url = url_mapping(url)
    while True:
        try:
            # proxy = get_proxy()
            # result = requests.get(url, proxies=proxy, timeout=3).json()
            result = requests.get(url).json()
            if result['Status'] != 1:
                logger.error('response status error!')
                continue
            # logger.info('%s upvotes: %s', proxy.get('http'), result['Count'])
            logger.info('upvotes: %s', result['Count'])
            if result['Count'] >= total_num:
                break
        except:
            logger.error('bad proxy!')

# def my_requests(url):
#     rs = (grequests.get(url, proxies=get_proxy(), timeout=5) for url in [url]*10)
#     grequests.map(rs)

def upvote(url, total_num):
    upvotes = Thread(target=_upvote, args=(url, total_num,))
    upvotes.setDaemon(True)
    upvotes.start()