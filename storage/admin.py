from django.contrib import admin
from .models import Storage

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ("user", "files", 'link' ,"date_created", "kunci")
    list_filter = ("date_created",)

    def link(self, obj):
        if obj.urls:
            return "<a href='%s'>Link</a>" % obj.urls
        else:
            ''