from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start', 'end')  # Fields to display in the admin interface
    search_fields = ('name',)  # Fields to enable searching in the admin interface

    def has_add_permission(self, request):
        return False  # Disable the "Add event" button

admin.site.register(Event, EventAdmin)
