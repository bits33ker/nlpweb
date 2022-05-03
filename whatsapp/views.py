# Create your views here.
from itertools import count
from django.shortcuts import render

from utils.utils import get_bar, get_hist, get_wordcloud

# Create your views here.
#from .models import Author, WhatsApp
# pasar al modelo
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.corpus import stopwords

from whatsapp.models import Contact, WhatsApp

def index(request):
    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_contacts = Contact.objects.all().count()
    wlist = WhatsApp.objects.all()
    num_whatsapp = WhatsApp.objects.all().count()
    transcripciones = []
    fechas = []
    texto = ''
    formato = '%Y-%m-%d'
    for a in wlist.iterator():
        f = a.get_datetime().strftime(formato)
        fechas.append(f)
        texto += a.get_message() + '. '
        transcripciones.append(a.get_message().encode("ascii", "ignore").decode())

    x = set(fechas)
    x = sorted(x)
    h = [fechas.count(i) for i in x]
    xp = x
    for i in range(0, len(x)
    ):
        if(i%10)!=0:
            xp[i]=''
    chart_whatsapp = get_bar(xp, h, 'WhatsApp per Date', 'Date', 'Counts')
    
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
    from sklearn.manifold import TSNE  
    from spacy.lang.es.stop_words import STOP_WORDS
    from spacy.lang.es import Spanish
    import spacy
    
    cv = TfidfVectorizer(ngram_range=(1,1), max_df=0.2, min_df=20, max_features=None, stop_words=STOP_WORDS)    
    chat_cv = cv.fit_transform(transcripciones)
    chat_freq = np.array(chat_cv.astype(bool).sum(axis=0)).flatten()
    chart_tfidf = get_hist(chat_freq, 'TfIdf', 'words', 'freq')

    chart_cloud = get_wordcloud(texto, STOP_WORDS)
    
    
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits': num_visits,
        'num_whatsapp': num_whatsapp,
        'num_contacts': num_contacts,
        'chart_whatsapp':chart_whatsapp,
        'chart_tfidf': chart_tfidf,
        'chart_cloud': chart_cloud,
        #'chart_topics': chart_topics,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'whatsapp.html', context=context)
