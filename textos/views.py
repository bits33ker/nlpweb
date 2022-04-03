from django.shortcuts import render

# Create your views here.
from .models import Audio

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_audios = Audio.objects.all().count()
    context = {
        'num_audios': num_audios,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
