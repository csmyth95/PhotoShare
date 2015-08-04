from django.conf.urls import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('polls.views',
                       # Examples:
                       url(r'^$', 'index'),
                       # url(r'^list/$', 'list', name='list'),
                       url(r'^profile/(?P<profile_id>\w+)/$', 'profile', name='profile'),
                       url(r'^login/$', 'user_login', name='login'),
                       url(r'^register/$', 'register', name='register'),
                       url(r'^about', 'about', name='about'),
                       url(r'^add_album/$', 'add_category', name='add_category'),
                       url(r'^logout/$', 'user_logout', name='logout'),
                       url(r'^album/(?P<category_name_url>\w+)/$', 'category', name='category'),
                       url(r'^album/(?P<category_name_url>\w+)/add_image/$', 'add_page', name='add_page'),
                       url(r'^goto/(?P<image_id>\w+)/$', 'track_url', name='track_url'),
                       url(r'^albums/$', 'albumlist', name='albumlist'),
                       url(r'^upload/$', 'upload', name='upload'),

             

                       url(r'^admin/', include(admin.site.urls)),
                       

                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
