"""blogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from app01 import views
from comments.views import comment
app_name = 'app01'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    # path('',views.index),
    path(r'texts/<int:pk>/',views.details,name='detail'),
    path(r'archives/<int:year>/<int:month>/',views.archive,name='archive'),
    path(r'cate/<int:pk>/',views.category,name='cate'),
    path(r'tags/<int:pk>/',views.tag,name='tag'),
    path(r'comment/<int:pk>/',comment,name='comment')
]
