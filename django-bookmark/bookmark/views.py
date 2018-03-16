from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect, resolve_url
from django.db.models import Q

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


from .serializers import BookmarkSerializer

from .models import *
import json

from . import summary

import logging
logger = logging.getLogger('django')
# logger.info('the_file: %s' % the_file)

# Create your views here.



class BookmarkViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    @method_decorator(csrf_exempt)
    def list(self, request):
        queryset = Bookmark.objects.all().order_by('-created')
        serializer = BookmarkSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, keyword=None):
        queryset = Bookmark.objects.filter(
            Q(title__icontains=keyword) | Q(description__icontains=keyword)).order_by('-created')

        serializer = BookmarkSerializer(queryset, many=True)
        return Response(serializer.data)

    def list_star(self, request):
        queryset = Bookmark.objects.filter(star=True).order_by('-created')
        serializer = BookmarkSerializer(queryset, many=True)
        return Response(serializer.data)

    def detail(self, request, pk):
        queryset = get_object_or_404(Bookmark, pk=pk)
        try:
            # queryset = Bookmark.objects.get(pk=pk)
            serializer = BookmarkSerializer(queryset)
            return Response(serializer.data)
        except queryset.DoesNotExist:
            return HttpResponse(status=404)

    def star(self, request, pk):
        b = get_object_or_404(Bookmark, pk=pk)
        try:
            b.star = False if b.star else True
            b.save()
            return HttpResponse(status=200)
        except b.DoesNotExist:
            return HttpResponse(status=404)

    def delete(self, request, pk):
        try:
            bookmark = Bookmark.objects.get(pk=pk).delete()
            return HttpResponse(status=200)
        except bookmark.DoesNotExist:
            return HttpResponse(status=404)
    
    def create(self, request):
        try:
            url = request.GET.get('url')
            data = summary.scrap(url)

            logger.info('summary.scrap(url)' % data)

            b = Bookmark.objects.create(
                url=data['url'],
                domain=data['domain'],
                title=data['title'],
                description=data['description'],
                image=data['image'],
                favicon=data['favicon']
            )
            serializer = BookmarkSerializer(b)
            return Response(serializer.data)
        except:
            return HttpResponse(status=404)



def serve_html(request, path):
    logger.info('path: %s' % path)
    return render(request, path)


def index(request, message=None):
    return render(request, 'index.html')



def scrap(request):
    url = request.GET.get('url')
    logger.info('[url] % s' % url)
    # try:
    #     data = summary.scrap(url)
    #     return JsonResponse(data)
    # except:
    #   return HttpResponse(status=404)

    data = summary.scrap(url)
    return JsonResponse(data)


