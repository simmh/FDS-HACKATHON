from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect, resolve_url
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q


from .models import *
import json

from . import summary

import logging
logger = logging.getLogger('django')
# logger.info('the_file: %s' % the_file)

# 데이터 직렬화 1
# def return_json():
#   return HttpResponse(json.dumps(data), content_type='application/json')

# qr 데이터 직렬화 2
# from django.http import JsonResponse
# def some_view(request):
#     data = list(SomeModel.objects.values())
#     return JsonResponse(data, safe=False)  # or JsonResponse({'data': data})

# Create your views here.

def obj_to_json(obj):
  data = serializers.serialize('json', [obj, ])
  struct = json.loads(data)
  data = json.dumps(struct[0], ensure_ascii=False)
  return data

def serve_html(request, path):
    logger.info('path: %s' % path)
    return render(request, path)

def index(request, message=None):
    return render(request, 'index.html')


def scrap(request):
  url = request.GET.get('url')
  try:
    data = summary.scrap(url)
  except:
    return JsonResponse({'status': 500})
  return HttpResponse(json.dumps(data), content_type='application/json')


def bookmark_view(request, word=None):
  if word == 'star':
    qs = Bookmark.objects.filter(star=True)
  if word and not word == 'star':
    qs = Bookmark.objects.filter(
        Q(title__icontains=word) | Q(description__icontains=word))
  if not word:
    qs = Bookmark.objects.all()
  qs_json = serializers.serialize('json', qs)
  return HttpResponse(qs_json, content_type='application/json')


def bookmark_detail_view(request, pk):
  try:
    data = get_object_or_404(Bookmark, pk=pk)

    res = {
      'status': 200,
      'data':{
          'id':data.id,
          'url': data.url,
          'domain': data.domain,
          'title': data.title,
          'image': data.image,
          'favicon': data.favicon,
          'star': data.star,
          'created': str(data.created),

      }
    }
  except:
    return JsonResponse({'status': 500, 'id': pk})
  return HttpResponse(json.dumps(res), content_type = 'application/json')




def bookmark_create_view(request):
  try:
    url = request.GET.get('url')
    data = summary.scrap(url)
    logger.info('summary.scrap(url)' % data)
    b = Bookmark.objects.create(url=data['url'], domain=data['domain'], title=data ['title'], description=data['description'], image=data['image'], favicon=data['favicon'])
  except:
    return JsonResponse({'status': 500})
  return HttpResponse(obj_to_json(b), content_type = 'application/json')
 

def bookmark_star_view(request, pk=None ):
  bookmark = Bookmark.objects.get(pk=pk)
  bookmark.star = False if bookmark.star else True
  bookmark.save()
  return JsonResponse({'status': 200, 'id':bookmark.pk, 'star': bookmark.star})


def bookmark_delete_view(request, pk):
  try:
    bookmark = Bookmark.objects.get(pk=pk).delete()
  except:
    return JsonResponse({'status': 500, 'id': pk})
  return JsonResponse({'status': 200, 'id': pk})


