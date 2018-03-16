"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework import routers
from bookmark import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
]


def viewz(mthd):
    return views.BookmarkViewSet.as_view({'get': mthd})

urlpatterns += [
    path('bookmarks/', viewz('list')),
    path('bookmarks/star/', viewz('list_star')),
    path('bookmarks/search/<str:keyword>/', viewz('retrieve')),

    path('bookmark/<int:pk>/', viewz('detail')),
    path('bookmark/star/<int:pk>/', viewz('star')),

    path('bookmark/delete/<int:pk>/', viewz('delete')),
    path('bookmark/create/', viewz('create')),

    path('summary', views.scrap),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
