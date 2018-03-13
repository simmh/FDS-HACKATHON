from urllib.parse import urlparse
from bs4 import BeautifulSoup
import metadata_parser
import bleach

# 0~3 불가 4~10
test_url =[
    # naver blog
    'https://blog.naver.com/bessgo/221227429246',
    'https://blog.naver.com/juneeeeeee/221225818069',
    #다음 블로그
    'http://blog.daum.net/leehungkyu/2176?bt_nil_d=0312_4',
    #egloos
    'http://runtorun.egloos.com/1263788',
    'http://poiemaweb.com/angular-component-style',
    'http://terms.naver.com/',
]

meta_data = {
    'title': None,
    'url': None,
    'domain': None,
    'image': None,
    'description': None,
    'fixed_url':None,
    'html_body':None,
}

one_img_site = [
    'twitter.com',
    # 'blog.naver.com',
    # 'm.blog.naver.com',
]


def summary(url):
    # metadata_parser third package 사용 추출
    page = metadata_parser.MetadataParser(url)
    data = {
        'title': page.get_metadata('title'),
        'url': page.get_metadata('url'),
        'image': page.get_metadata('image'),
        'description': page.get_metadata('description'),
        'domain': page.get_metadata('domain'),
        'html': None
        
    }

    print([metadata_parser], data)

    # url 파싱
    parsed_url = urlparse(url)  

    # 도메인 없다면 추가
    if not data['domain']:
        data['domain'] = parsed_url.scheme + '://' + parsed_url.netloc
    
    if is_except_url(url):
        data['html'] = to_html_bs(url)
        
    return data

    
def to_html_bs(url, o=None):
    # hdr = {'User-Agent': 'Mozilla/5.0', 'referer' :'http://m.naver.com' }
    headers = {
        'Referer': url,
        'user-agent': 'my-app/0.0.1',
    }
    headers2 = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Referer': 'http://aussietaste.recipes/vegetables/leek-vegetables/leek-and-sweet-potato-gratin/'
    }

    try:
        html = requests.get(url, headers=headers).text
        html_bs = BeautifulSoup(html, 'html.parser')
    except:
        html_bs = None
    return html_bs
    
    
def is_except_url(url):
    naver_attrs = {'id':'mainFrame'}
    daum_attrs = {'name':'BlogMain'}

    except_url ={
        # naver
        'blog.naver.com':naver_attrs,
        'm.blog.naver.com':naver_attrs,
        # daum
        'blog.daum.net': daum_attrs,
        'm.blog.daum.net': daum_attrs,
    }
    
    if parsed_url.netloc in except_url.keys():
        return True 
    else: 
        return False
    
def exists(url, domain_url, o=None):
    def status_check(url):
        try:
            r = requests.head(url)
            if r.status_code == requests.codes.ok:
                return True
        except:
            pass
        return False

    if status_check(url):
        logger.info('[status_check]: ok %s' % url)
        return url
    
    return False
    
def body_parse(html):
    title = html.find('title').text
    body = html.find_all('p', limit=20)
    # logger.info('[body_parse] body: %s' % body)
#     body2 = ' '.join(body)
#     logger.info('body2: %s' % body2)
    body = bleach.clean(body, strip=True)
    body = BeautifulSoup(body, 'html.parser')

    for a in body.find_all('a'):
        del a['href']

    data = {
        'title': title,
        'description': body.text[:300],
    }
    return data


# 3
summary(test_url[1])







