# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'', include('error.urls')),
    (r'', include('receiving.urls')),
    (r'', include('app.urls')),
    (r'', include('users.urls')),
    (r'^stats/', include('stats.urls')),
    (r'^projects/', include('projects.urls')),
    (r'^notification/', include('notifications.urls')),
)

handler404 = 'app.errors.not_found_error'
handler500 = 'app.errors.application_error'