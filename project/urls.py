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

from bookmark import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('bookmark/', views.bookmark_view, name='bookmark_list'),
    path('bookmark/search/<str:word>', views.bookmark_view, name='bookmark_create'),
    path('bookmark/<int:pk>/', views.bookmark_detail_view, name='bookmark_detail'),
    path('bookmark/create/', views.bookmark_create_view, name='bookmark_create'),
    # path('bookmark/delete/<int:pk>/', views.bookmark_delete_view, name='bookmark_delete'),
    path('bookmark/update/<int:pk>/', views.bookmark_update_view, name='bookmark_update'),
    
    path('scrap/', views.scrap, name='scrap')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
