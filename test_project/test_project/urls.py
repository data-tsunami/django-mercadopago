from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'test_app.views.home', name='home'),
    url(r'^mp/', include('djmercadopago.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
