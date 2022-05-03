from django.db import models
from uuid import uuid4 as uuid4

# Create your models here.
class Contact(models.Model):
    #contact_id = models.UUIDField(primary_key=True, default=uuid4, help_text='Unique ID for this particular WhatsApp Contact')
    name = models.TextField(verbose_name='contact', help_text='Contact of whatsapp')
    
    class Meta:
       db_table = 'Contact'

    def __str__(self):
        return f'{self.name}'
    
class WhatsApp(models.Model):
    #whatsapp_id = models.UUIDField(primary_key=True, default=uuid4, help_text='Unique ID for this particular WhatsApp Message')
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    whatsappgroup = models.ForeignKey('WhatsAppGroup', on_delete=models.CASCADE)
    dt_message= models.DateTimeField(help_text='WhatsApp datetime')
    message=models.CharField(max_length=1024, help_text='whatsapp message')

    class Meta:
       db_table = 'WhatsApp'
       ordering = ['dt_message']
    
    def __str__(self):
        return f'{self.dt_message}, {self.contact}, {self.message}'
    
    def get_message(self):
        return self.message
    def get_datetime(self):
        return self.dt_message

class WhatsAppGroup(models.Model):
    #group_id = models.UUIDField(primary_key=True, default=uuid4, help_text='Unique ID for this particular WhatsApp group')
    name = models.TextField(verbose_name='group', help_text='Group of whatsapp')

    def __str__(self):
        return f'{self.name}'
    