from django.conf.urls import url
from . import views


urlpatterns = [
    url('', views.AskLuga.as_view(), name='index')
]
