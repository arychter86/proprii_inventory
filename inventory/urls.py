"""proprii URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from . import views
from inventory.views import *
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
# ... your normal urlpatterns here

urlpatterns = [
     url(r'^$', login_required(InventoryList.as_view())),
     url(r'^inventory/(?P<id>[0-9]+)/$', login_required(InventoryView.as_view())),
     url(r'^inventory/add/$', login_required(InventoryView.as_view())),
     url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='auth_logout'),
     url(r'^login/$', auth_views.login, name='login'),
     url(r'^inventory/(?P<id>[0-9]+)/tree/(?P<id_t>[0-9]+)/$', login_required(TreeView.as_view())),
     url(r'^inventory/(?P<id>[0-9]+)/tree/(?P<id_t>[0-9]+)/snap/$', login_required(TreeImageView.as_view())),
     url(r'^inventory/(?P<id>[0-9]+)/tree/(?P<id_t>[0-9]+)/image/(?P<id_image>[0-9]+)/delete/$', login_required(TreeImageDeleteView.as_view())),
     url(r'^inventory/(?P<id>[0-9]+)/tree/(?P<id_t>[0-9]+)/delete/$', login_required(TreeDeleteView.as_view())),
     url(r'^inventory/(?P<id>[0-9]+)/tree/(?P<id_t>[0-9]+)/trunk/(?P<id_tt>[0-9]+)/delete/$', login_required(TreeTrunkDeleteView.as_view())),
     url(r'^inventory/(?P<id>[0-9]+)/tree/$', login_required(TreeView.as_view())),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
