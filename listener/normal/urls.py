from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

import os
from django.conf import settings

urlpatterns = patterns('',
    (r'', include('error.urls')),
    (r'', include('receiving.urls')),
    (r'', include('app.urls')),
    (r'', include('users.urls')),
    (r'^stats/', include('stats.urls')),
    (r'^projects/', include('projects.urls')),
    (r'^notification/', include('notifications.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)', 'django.views.static.serve',
     {'document_root' : os.path.join(settings.ROOT_PATH, '..', 'media')})
)

#handler404 = 'app.errors.not_found_error'
#handler500 = 'app.errors.application_error'
