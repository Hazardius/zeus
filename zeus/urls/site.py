from django.conf.urls import include, patterns, url

urlpatterns = patterns('zeus.views.site',
    url(r'^$', 'home', name='home'),
    url(r'^stvcount/$', 'stv_count', name='stv_count'),
    url(r'^terms/$', 'terms', name='terms'),
    url(r'^faqs/$', 'faqs_voter', name='faqs'),
    url(r'^faqs/voter/$', 'faqs_voter', name='faqs_voter'),
    url(r'^faqs/trustee/$', 'faqs_trustee', name='faqs_trustee'),
    url(r'^resources/$', 'resources', name='site_resources'),
    url(r'^contact/$', 'contact', name='site_contact'),
    url(r'^stats/$', 'stats', name='site_stats'),
    url(r'^demo$', 'demo', name='site_demo'),
    url(r'^error/(?P<code>[0-9]+)$', 'error', name='error')
)
