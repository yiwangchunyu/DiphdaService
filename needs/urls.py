"""DiphdaService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path, re_path, include

from needs import views

urlpatterns = [
    re_path(r'^create$', views.create),
    re_path(r'^update', views.update),
    re_path(r'^delete', views.show),
    re_path(r'^show', views.show),
    re_path(r'^getTags$', views.getTags),
    re_path(r'^getCategories$', views.getCategories),
    re_path(r'^listOrder$',views.listOrder),
    re_path(r'^createOrder$',views.createOrder),
    re_path(r'^cancelOrder$',views.cancelOrder),
    re_path(r'^updateOrder$',views.updateOrder),
    re_path(r'^orderDetail$',views.orderDetail),
]
