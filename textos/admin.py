from django.contrib import admin

# Register your models here.
from .models import Audio

#admin.site.register(Audio)

# Define the admin class
class AudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'transcript')

# Register the admin class with the associated model
admin.site.register(Audio, AudioAdmin)
