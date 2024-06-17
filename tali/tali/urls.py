"""
URL configuration for tali project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth.views import LoginView

from rest_framework.routers import DefaultRouter
from homepage import views

router = DefaultRouter()
router.register(r'users', views.myUserViewSet, basename='myuser')
router.register(r'posts', views.PostViewSet, basename='Post')


urlpatterns = [
    # path receives 4 args: 'route':str, 'view', 'kwargs':dict, 'name' - unambiguous refrence (see example in polls.urls.py)
    path("", include("homepage.urls")),
    path("admin/", admin.site.urls),
    path('login/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
