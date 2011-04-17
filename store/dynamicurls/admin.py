from django.contrib import admin
from dynamicurls.models import UrlString, TinyUrlString

admin.site.register(UrlString)
admin.site.register(TinyUrlString)