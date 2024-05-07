from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

# adding an app_name makes the below 'names' fall under the namespace polls - e.g polls:index, polls:detail etc.
# when the name is used in templates
app_name = "homepage"

urlpatterns = [
    path("", views.index, name="index"),
    path('api/', include(router.urls)),
]
