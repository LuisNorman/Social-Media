"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views # make sure to import views
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage.as_view(), name='home'), # link homepage
    path('accounts/', include('accounts.urls', namespace='accounts')), # when someone signs in and gets directed to accounts.urls
    path('accounts/', include('django.contrib.auth.urls')), # allows us to connect to django's authorization
    path('test/', views.TestPage.as_view(), name='test'),
    path('thanks/', views.ThanksPage.as_view(), name='thanks'),
    path('posts/', include('posts.urls', namespace='posts')),  # register the namespace posts so the server knows what to do when going to /posts/
    path('groups/', include('groups.urls', namespace='groups')),
]
