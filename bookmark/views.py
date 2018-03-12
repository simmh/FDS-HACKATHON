from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect, resolve_url
from .models import *
# from .forms import *
import json

from . import scrap0

import logging
logger = logging.getLogger('django')
# logger.info('the_file: %s' % the_file)

# def return_json():
#   return HttpResponse(json.dumps(data), content_type='application/json')

# Create your views here.

def serve_html(request, path):
    logger.info('path: %s' % path)
    return render(request, path)

def scrap(request):
  # url = request.GET.get('url')
  url = 'https://www.acmicpc.net/blog/view/16'
  data = scrap0.summary(url)
  return HttpResponse(json.dumps(data), content_type='application/json')
  # return HttpResponse(data)

def bookmark_view():
  return

def bookmark_detail_view():
  return

def bookmark_create_view():
  return

def bookmark_update_view():
  return

