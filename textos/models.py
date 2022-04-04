from django.db import models

# Create your models here.
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models#summary
class Audio(models.Model):
    name = models.CharField(max_length=200, help_text='Wav filename')
    filesize = models.IntegerField(verbose_name='wav_filesize')
    transcript = models.TextField(verbose_name='transcript')

    class Meta:
        ordering = ['name', 'transcript']


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}, {self.transcript}'

    def get_transcript(self):
        return self.transcript