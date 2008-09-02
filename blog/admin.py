from django.contrib import admin
from models import Entry, File

class BasicAdmin(admin.ModelAdmin):
    pass

admin.site.register(Entry, BasicAdmin)
admin.site.register(File, BasicAdmin)
