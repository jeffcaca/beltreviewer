from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
  	url(r"add$", views.addbook, name="addbook"),
  	url(r"addbook$", views.addbookreview, name="addbookreview"),
 	url(r"^(?P<id>\d+)", views.viewbook, name="viewbook"),
 	url(r"users/(?P<id>\d+)", views.showuser, name="showuser"),
 	url(r"addreview/(?P<id>\d+)", views.addreview, name="addreview"),
]