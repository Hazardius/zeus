from django.conf.urls.defaults import *

urlpatterns = patterns('zeus.views.site',
    url(r'^$', 'home', name='home'),
    url(r'^faqs/$', 'faqs_voter', name='faqs'),
    url(r'^faqs/voter/$', 'faqs_voter', name='faqs_voter'),
    url(r'^faqs/trustee/$', 'faqs_trustee', name='faqs_trustee'),
    url(r'^resources/$', 'resources', name='site_resources'),
    url(r'^stats/$', 'stats', name='site_stats'),
    url(r'^demo$', 'demo', name='site_demo')
)
