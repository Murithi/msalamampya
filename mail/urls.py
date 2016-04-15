__author__ = 'eric'


from django.conf.urls import include, url
from django.contrib import admin
from django_messages.views import inbox, view, reply, delete, outbox, compose

urlpatterns = [
    url(r'^inbox/$', inbox, {'template_name': 'mail.html',}, name='messages_inbox'),
    url(r'^view/(?P<message_id>[\d]+)/$', view, {'template_name': 'viewmail.html',}, name='messages_detail'),
    url(r'^reply/(?P<message_id>[\d]+)/$', reply,  name='messages_reply'),
    url(r'^delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
    url(r'^outbox/$', outbox, {'template_name': 'outbox.html',}, name='messages_outbox'),

    url(r'^compose/$', compose, name='messages_compose'),
    url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
    # url(r'^view/(?P<message_id>[\d]+)/$', view, name='messages_detail'),
]
