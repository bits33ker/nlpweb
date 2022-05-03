import random
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# https://www.google.com/search?q=django+display+plots&oq=django+view+plot&aqs=chrome.1.69i57j0i22i30.14860j0j4&sourceid=chrome&ie=UTF-8#kpvalbx=_z-RKYoL8Hf2I4dUP7buA-AE17
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_hist(h, title, xlabel, ylabel):
    plt.switch_backend('AGG')
    plt.figure(figsize=[10,5])
    plt.title(title)
    #plt.plot(x, y)
    plt.hist(h, bins=100,log=True)
    plt.xticks(rotation=45)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_bar(x, h, title, xlabel, ylabel):
    plt.switch_backend('AGG')
    plt.figure(figsize=[10,5])
    plt.title(title)
    #plt.plot(x, y)
    plt.bar(x, h, width = 1, color='#0504aa',alpha=0.7)
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(rotation=45)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=[10,5])
    plt.title('Vocab freqs')
    plt.plot(x, y)
    #plt.hist(h, bins=100,log=True)
    plt.xticks(rotation=45)
    plt.xlabel('Vocab')
    plt.ylabel('freqs')
    plt.tight_layout()
    graph = get_graph()
    return graph

# https://www.aprendemachinelearning.com/ejercicio-nlp-cuentos-de-hernan-casciari-python-espanol/
from wordcloud import WordCloud
def get_wordcloud(t, stop_words):
    #stop_words = ['de', 'la', 'y', 'que', 'a', 'el', 'un', 'con', 
    #    'su', 'se', 'no', 'si', 'las', 'por', 'lo', 'en', 'los', 'al',
    #    'del', 'me', 'le', 'mi', 'como', 'una', 'yo', 'para', 'todo', 'e', 
    #    'mas', 'sus', 'era', 'habia', 'este', 'esta', 'tan', 'esto']
    wc = WordCloud(stopwords=stop_words, background_color='white', colormap='Dark2', 
        max_font_size=150, random_state=42)
    wc.generate(t)
    plt.figure(figsize=[10,5])
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    graph = get_graph()
    return graph

import pyLDAvis
def get_topics(lda, chat_cv, cv):
    pyLDAvis.enable_notebook()
    dash = pyLDAvis.sklearn.prepare(lda, chat_cv, cv, mds='tsne')
    return dash