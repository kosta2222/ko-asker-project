import bs4 as bs
import urllib.request
import nltk
from nltk.corpus import stopwords
from gensim.models import Word2Vec
import re
import os
import json

vec_size = 10  # размер вектора слова от word2vec обработки
input_articles_fname = 'I.txt'  # файл с урлами статей из википедии
# создаем папки на уровне скрипта
word2vec_model_save_folder = 'word2vec_model_save_folder'
cache_articles = 'cache.txt'
nn_model_trained_save_folder = 'nn_model_trained_save_folder'
nepochs_word2vec = 10
seed_word2vec = 42
min_count_word2vec = 0
fname_2test_nn1 = 'test_article_calculation.txt'
fname_2test_nn2 = 'test_article_printing.txt'
fname_saved_nn = 'articles_wiki.xml'


def article_tokenize(article_text: str):
    # Cleaing the text
    processed_article = article_text.lower()
    processed_article = re.sub('[^a-zA-Z]', ' ', processed_article)
    processed_article = re.sub(r'\s+', ' ', processed_article)
    # Preparing the dataset
    all_sentences = nltk.sent_tokenize(processed_article)
    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
    # Removing Stop Words
    len_all_words = len(all_words)
    for i in range(len_all_words): # get 2D matrix
        all_words[i] = [
            w for w in all_words[i]  
            if w not in stopwords.words('english')
        ]
    return all_words


def train_word2vec(all_words: list):
    # accepts 2D list
    word2vec = Word2Vec(all_words,
                        min_count=min_count_word2vec,
                        size=vec_size,
                        iter=nepochs_word2vec,
                        seed=seed_word2vec)
    return word2vec


articles_json = {}


def read_article_2cache_article_3train_word2vec_article_4return_learned_model(url: str):
    
    scrapped_data = urllib.request.urlopen(url)
    article = scrapped_data.read()
    parsed_article = bs.BeautifulSoup(article, 'lxml')
    paragraphs = parsed_article.find_all('p')

    article_text = ""
    for p in paragraphs:
        article_text += p.text
    all_words = article_tokenize(article_text)

    name = url.split('/')[-1]
    articles_json[name] = all_words
    with open(cache_articles, mode='w', encoding='utf8') as f:
        json.dump(articles_json, f)

    model=train_word2vec(all_words)

    return model


def read_cache_or_read_urls_2train_word2vec_models_3save_word2vec_models():
    if os.path.exists('%s'%cache_articles):
        print('read cache')
        articles=json.load(open(cache_articles))
        # save word2vec models
        for i in articles.items(): 
            word2vec=train_word2vec(i[1])
            wv=word2vec.wv
            wv.save(os.path.join(word2vec_model_save_folder, i[0]))
    else:
        print('%s did not faind'%cache_articles)
        urls: list = None
        with open(input_articles_fname, 'r') as f:
          urls = f.readlines()

        # save word2vec models
        for url in urls:
            url = url.strip().rstrip('\r\n')
            saved_model_fname = url.split('/')[-1] + '.vks'
            word2vec = read_article_2cache_article_3train_word2vec_article_4return_learned_model(url)
            wv=word2vec.wv
            wv.save(
                os.path.join(word2vec_model_save_folder, saved_model_fname))

           

read_cache_or_read_urls_2train_word2vec_models_3save_word2vec_models()
