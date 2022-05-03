from django.shortcuts import render

from utils.utils import get_wordcloud

# Create your views here.
from .models import Audio
# pasar al modelo
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.corpus import stopwords

def index(request):
    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Generate counts of some of the main objects
    num_audios = Audio.objects.all().count()
    transcripciones = []
    texto = ''
    lista = Audio.objects.all()
    limite = 1000
    i = 0
    for a in lista.iterator():
        texto += a.get_transcript() + '. '
        transcripciones.append(a.get_transcript().encode("ascii", "ignore").decode())
        i = i + 1
        if i>=limite:
            break

    cv = TfidfVectorizer(ngram_range=(1,1), max_df=0.2, min_df=20, max_features=None)
    transcript_cv = cv.fit_transform(transcripciones)
    num_vocab = len(cv.get_feature_names())
    vocab_freq = np.array(transcript_cv.astype(bool).sum(axis=0)).flatten()
    #chart = get_hist(vocab_freq)
    chart = get_wordcloud(texto)
    context = {
        'num_visits': num_visits,
        'num_audios': num_audios,
        'num_vocab': num_vocab,
        'transcripciones': texto,
        'chart': chart,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
