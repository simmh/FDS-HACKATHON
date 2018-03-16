from urllib.parse import urlparse
from bs4 import BeautifulSoup
import metadata_parser
import requests
import logging
logger = logging.getLogger('django')
# logger.info('file: %s' % file)

# meta site
# url = 'http://www.naver.com'
# url = 'http://poiemaweb.com/angular-component-style'
# url = 'http://terms.naver.com/'
# url = 'https://twitter.com/sheispuzzled/status/973207418548072448'
# url = 'http://akul.me/blog/2016/beautifulsoup-cheatsheet/'

# naver blog
# url = 'https://blog.naver.com/bessgo/221227429246'
# url = 'https://blog.naver.com/juneeeeeee/221225818069'

# daum blog
# url = 'http://blog.daum.net/leehungkyu/2176?bt_nil_d=0312_4'

#egloos
# url = 'http://runtorun.egloos.com/1263788'




def scrap(url):
    parsed_url = urlparse(url)     

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

    html = None
    html_bs = None

    def get_html_and_bs(url):   
        headers = {'Referer': url,'user-agent': 'my-app/0.0.1'}
        headers2 = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Referer': 'http://aussietaste.recipes/vegetables/leek-vegetables/leek-and-sweet-potato-gratin/'
        }

        html = requests.get(url, headers=headers2).text
        html_bs = BeautifulSoup(html, 'html.parser')
        return {'html': html, 'bs': html_bs}




    # ParseResult(scheme='http', netloc='www.naver.com', path='', params='', query='', fragment='')
    def is_except_url(parsed_url):   
        if parsed_url.netloc in except_url.keys():        
            return except_url[parsed_url.netloc]           
        return False


    


    def get_except_url_in_source(url, parsed_url):
        attrs = is_except_url(parsed_url)
        bs =  get_html_and_bs(url)['bs']
    #     set_html_and_bs(url)
        source_url = bs.find("frame", attrs )['src']
        source_url = parsed_url.scheme + '://' + parsed_url.netloc + source_url
        return source_url

    def status_check(url):
        r = requests.head(url)
        if r.status_code == requests.codes.ok:
            return True
        return False


    # def get_metadata_parser(url):
    #     page = metadata_parser.MetadataParser(url)
    #     data = {
    #             'title': page.get_metadata('title'),
    #             'url': page.get_metadata('url'),
    #             'image': page.get_metadata('image'),
    #             'description': page.get_metadata('description'),
    #         }
    #     return data


    def get_metadata_parser(url):
        def set_metadata(page):            
            data = {
                'title': page.get_metadata('title'),
                'url': page.get_metadata('url'),
                'image': page.get_metadata('image'),
                'description': page.get_metadata('description'),
            }
            return data

        try:
            page = metadata_parser.MetadataParser(url)
            data = set_metadata(page)
        except:
            data = None

        if not data:
            try:
                page = metadata_parser.MetadataParser(html=html)
                data = set_metadata(page)
            except:
                data = None

        return data



    def custom_parser(bs = get_html_and_bs(url)['bs']):
        title = bs.find('title').text
        body = bs.find_all('p', limit=10)
        strip_body = ''
        for b in body:
            strip_body += b.text
        return {'title': title, 'body': strip_body}

    if is_except_url(parsed_url):
        data = get_metadata_parser(get_except_url_in_source(url, parsed_url))
    else:        
        data = get_metadata_parser(url)

    def get_favicon():
        try:
            bs = get_html_and_bs(url)['bs']
            # logger.info('get_favico: %s' % bs)
            fvc_url = bs.find(rel='icon').get('href')
            fvc_parsed_url = urlparse(fvc_url)
        except:
            logger.info('get_favico Fail')
            return None
        

        if not fvc_parsed_url.netloc:
            fvc_url = parsed_url.scheme + '://' + parsed_url.netloc + fvc_url
        return fvc_url
        # link rel = shorcuticon href



        
    if not data['title']:
        data['title'] = custom_parser()['title']

    if not data['description']:
        data['description'] = custom_parser()['body']

    if data['image']:
        img_parsed_url = urlparse(data['image'])
        if not img_parsed_url.netloc:
            data['image'] = img_parsed_url.scheme + \
                '://' + parsed_url.netloc + data['image']

    
    
    meta_data = {
        'url': url,
        'domain': parsed_url.netloc,
        'title': data['title'],
        'description': data['description'],
        'image': data['image'],
        'favicon': get_favicon(),
#         'source_url':,
    }
    logger.info('[SUMMARY meta_data]: %s' % meta_data)
    
    return meta_data

# summary(url)
