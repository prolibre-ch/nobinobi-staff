# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('nobinobi_staff.urls', namespace='nobinobi_staff')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
