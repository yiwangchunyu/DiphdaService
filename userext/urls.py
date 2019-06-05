from django.urls import path, re_path, include

from userext import views

urlpatterns = [
    # re_path(r'^update', views.update),
    re_path(r'^get$', views.get),
    re_path(r'^addExpc$', views.addExpc),
]