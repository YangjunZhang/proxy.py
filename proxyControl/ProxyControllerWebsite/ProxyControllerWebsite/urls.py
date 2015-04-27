from django.conf.urls import include, url
from django.contrib import admin
from ProxyControllerWebsite.views import hello

urlpatterns = [
    # Examples:
    # url(r'^$', 'ProxyControllerWebsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ProxyController/', include('ProxyController.urls')),
    url(r'^hello/', hello),
]
