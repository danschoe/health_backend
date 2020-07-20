from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('disorder/<str:name>', views.disorder_name, name='disorder_name'),
    path('diagnostic', views.diagnostic, name='diagnostic'),
    # path('^diagnostic/$', csrf_exempt(views.diagnostic), name='diagnostic'),
]
