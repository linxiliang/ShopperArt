from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^dumbhead/', include('dumbhead.urls')),
    url(r'^admin/', admin.site.urls),
]
