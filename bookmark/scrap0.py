from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import metadata_parser
import bleach
import logging
logger = logging.getLogger('django')
# logger.info('file: %s' % file)

naver_attrs = {'id': 'mainFrame'}
daum_attrs = {'name': 'BlogMain'}
ex_url = {
    # naver
    'blog.naver.com': naver_attrs,
    'm.blog.naver.com': naver_attrs,
    # daum
    'blog.daum.net': daum_attrs,
    'm.blog.daum.net': daum_attrs,
}

one_img_site = [
    'twitter.com',
    # 'blog.naver.com',
    # 'm.blog.naver.com',
]


def summary(url):
    fixed_url = None
    o = urlparse(url)
    html = url_to_html(url, o)
    domain_url = o.scheme+'://'+o.netloc

    if o.netloc in ex_url.keys():
        try:
            fixed_url = html.find('frame', attrs=ex_url[o.netloc])['src']
            fixed_url = exists2(fixed_url, domain_url)
            if fixed_url:
                # if not exists(fixed_url):
                #     return HttpResponseBadRequest(_('no requets.get fixed url'))
                html = url_to_html(fixed_url)
        except:
            # return HttpResponseBadRequest(_('no requets.get fixed url'))
            pass
    # else:
    #     if not exists(url):
    #         return HttpResponseBadRequest(_('no requets.get fixed url'))
            # return HttpResponseBadRequest('no requets.get fixed url', mimetype = 'application/json', status = 409)

    if fixed_url:
        data = meta_data(fixed_url)
    else:
        data = meta_data(url)

    if not data['description']:
        data = meta_og_parse(html)

    if not data['description']:
        data = body_parse(html)

    data['domain_url'] = domain_url
    data['domain'] = o.netloc
    data['fixed_url'] = fixed_url
    data['img_list'] = None

    # 타이틀 이미지 1개 사이트 여부 검사
    if not o.netloc in one_img_site:
        # 웹페이지 이미지 리스트 생성
        img_list = img_parse(html, domain_url)
        if img_list:
            data['image'] = img_list[0]
            data['img_list'] = img_list

    return data
    # return HttpResponseBadRequest(_('no requets.get fixed url'))


def meta_data(url=None, html=None):
    def get_page_data(page):
        data = {
            'title': page.get_metadata('title'),
            'url': page.get_metadata('url'),
            'image': page.get_metadata('image'),
            'description': page.get_metadata('description'),
        }
        return data

    try:
        page = metadata_parser.MetadataParser(url=url)
        data = get_page_data(page)
    except:
        data = None

    if not data:
        try:
            page = metadata_parser.MetadataParser(html=html)
            data = get_page_data(page)
        except:
            data = None

    return data


def url_to_html(url, o=None):
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
        bs = BeautifulSoup(html, 'html.parser')
    except:
        bs = None
    return bs


def meta_og_parse(html):
    try:
        title = html.find('meta', attrs={'property': 'og:title'})['content']
    except:
        title = None

    try:
        description = html.find(
            'meta', attrs={'property': 'og:description'})['content']
    except:
        description = None

    data = {
        'title': title,
        'description': description,
    }
    return data


def body_parse(html):
    title = html.find('title').text
    body = html.find_all('p', limit=20)
    body = bleach.clean(body, strip=True)
    body = BeautifulSoup(body, 'html.parser')

    for a in body.find_all('a'):
        del a['href']

    data = {
        'title': title,
        'description': body.text[:300],
    }
    return data


def exists(url):
    try:
        r = requests.head(url)
        if r.status_code == requests.codes.ok:
            return True
    except:
        pass
    return False


def exists2(url, domain_url, o=None):
    def status_check(url):
        try:
            r = requests.head(url)
            if r.status_code == requests.codes.ok:
                return True
        except:
            pass
        return False

    if status_check(url):
        logger.info('status_check: ok %s' % url)
        return url
    else:
        if not o:
            logger.info('status_check: o:none %s' % url)
            o = urlparse(url)

        if not o.scheme and o.netloc:
            # f_url = 'http://'+o.geturl()
            f_url = 'http://' + o.netloc + o.path + o.params + o.query + o.fragment
            if status_check(f_url):
                return f_url

        if not o.netloc:
            f_url = domain_url + o.geturl()
            logger.info('status_check: f_url %s' % f_url)
            if status_check(f_url):
                return f_url

    return


def img_parse(html, domain_url):
    ('start img parse!: ')

    def img_check(src):
        ('chek start src!: %s' % src)
        if exists(src):
            ('exists img!!: %s' % src)
            return src
        else:
            src_o = urlparse(src)
            if not src_o.netloc:
                f_src = domain_url + src_o.path
                logger.info('f_src: %s' % f_src)
                if exists(f_src):
                    return f_src
        return

    def allow_img(src, o):
        allow = ('jpg', 'png')
        not_allow = ()
        if o.path.endswith(allow):
            return True
        return False
        # if not o.path.endswith('gif'):
        #     return True
        # return False

    def meta_img_parse(html):
        meta_img = html.find_all('meta', attrs={'property': 'og:image'})
        meta_img_list = []

        for i in meta_img:
            src_o = urlparse(i['content'])
            logger.info('beafore meta img append: %s' % i['content'])
            # checked_src = img_check(i['content'])
            checked_src = exists2(i['content'], domain_url, src_o)
            logger.info('checked meta img: %s' % checked_src)
            if checked_src:
                logger.info('meta img append: %s' % checked_src)
                meta_img_list.append(checked_src)

        return meta_img_list

    def html_img_parse(html):
        if html.find('body'):
            html_img = html.find("body").find_all('img')[:50]
        else:
            html_img = html.find_all('img')[:50]
        logger.info('html_img: %s' % html_img)
        html_img_list = []
        for idx, i in enumerate(html_img):
            try:
                src_o = urlparse(i['src'])
                logger.info('beafore html img i[src]: %s' % i['src'])
                # checked_src = img_check(i['src'])
                checked_src = exists2(i['src'], domain_url, src_o)
                allow_check = allow_img(checked_src, src_o)
                logger.info('beafore html img append: %s' % checked_src)
                logger.info('allow check: %s' % allow_check)

                # if checked_src:
                if checked_src and allow_check:
                    logger.info('>>>>html img append: %s' % checked_src)
                    html_img_list.append(checked_src)
            except:
                pass

            if idx == 30:
                break

        return html_img_list

    m_list = meta_img_parse(html)
    h_list = html_img_parse(html)
    img_list = m_list + h_list

    # logger.info('html img: %s' % html)
    # logger.info('m_list: %s' % m_list)
    # logger.info('h_list: %s' % h_list)
    # logger.info('img_list: %s' % img_list)
    return img_list


url = 'https://recall2300.github.io/2016-12-27/pip-freeze/'
print(summary(url))
