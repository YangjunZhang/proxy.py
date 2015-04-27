from django.conf.urls import include, url
from ProxyController.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'ProxyControllerWebsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^hello/', hello),
    url(r'^status/', status),
    url(r'^query', query),
    url(r'^files', files),
]
