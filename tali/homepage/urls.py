from django.urls import path

from . import views

# adding an app_name makes the below 'names' fall under the namespace polls - e.g polls:index, polls:detail etc.
# when the name is used in templates

urlpatterns = [
    path("", views.index, name="index"),
]
