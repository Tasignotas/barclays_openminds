from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'creative_exchange.views.trading', name='home'),

    url(r'^traders/login/$', 'django.contrib.auth.views.login'),
    url(r'^get_trade_and_order', 'creative_exchange.views.get_trade_and_order'),
    url(r'^traders/logout/$', 'django.contrib.auth.views.logout_then_login', kwargs={ 'login_url': '/' }),
    
    url(r'^traders/profile/$', 'creative_exchange.views.trader_test'),

    url(r'^admin/', include(admin.site.urls)),
)
