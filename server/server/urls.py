from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'creative_exchange.views.trading', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^traders/login/$', 'django.contrib.auth.views.login'),

    url(r'^admin/', include(admin.site.urls)),
)
