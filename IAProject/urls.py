from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IAProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$', 'crawl.views.hello_world'),
    url(r'^$','crawl.views.index'),
    url(r'^crawlSite','crawl.views.crawlSite'),
    url(r'^showtime','crawl.views.showtime'),
)
