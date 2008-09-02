from django.contrib import admin
from models import Entry, File

class BasicAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_date'
    list_filter = ['private']

admin.site.register(Entry, EntryAdmin)
admin.site.register(File, BasicAdmin)
