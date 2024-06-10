from django.conf import settings
from django.urls import path, include

from . import views
from django.contrib.auth.views import LogoutView

from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'users', views.myUserViewSet, basename='myuser')
# router.register(r'posts', views.PostViewSet, basename='Post')

# adding an app_name makes the below 'names' fall under the namespace polls - e.g polls:index, polls:detail etc.
# when the name is used in templates
app_name = "homepage"

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('check_email/', views.check_email, name='check_email'),
    path('activate/<str:pk>', views.TalisActivationView.as_view(), name='activate'),
    # path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('login/', include('django.contrib.auth.urls')),  
    path('login/logout/', views.do_logout, name='logout'),
    path('login/login/', views.do_logout, name='login'),
]
