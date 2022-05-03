from django.contrib import admin

# Register your models here.
from .models import  WhatsApp, Contact

#admin.site.register(Audio)

# Define the admin class
class WhatsAppAdmin(admin.ModelAdmin):
    list_display = ('dt_message', 'contact_id', 'message')

#class ContactAdmin(admin.ModelAdmin):
#    list_display = ('contact_id','name')

# Register the admin class with the associated model
admin.site.register(WhatsApp, WhatsAppAdmin)
#admin.site.register(Contact, ContactAdmin)
