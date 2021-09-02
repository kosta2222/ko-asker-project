from command_pat import shell
from command_pat._command import Command
import os
import sys
import json
from gensim.models import KeyedVectors


word2vec_model_save_folder = 'word2vec_model_save_folder'
cache_articles = 'cache.txt'


class PrintArticleTokenize(Command):
    def __init__(self):
        self.cache=os.path.join(os.path.dirname(sys.executable), '..', cache_articles)

    def execute(self, args):
        name=args[0]
        words=json.load(open(self.cache))
        article=words[name][0]
        print(article)
        return 0

    def __repr__(self):
        return """Prints articles tokenize 
        (usage: <args> -> <article name without extension>)""" 


class GemsimW2vSimilarWords(Command):
    def __init__(self):
       self.model=os.path.join(os.path.dirname(sys.executable), '..', word2vec_model_save_folder)
    def execute(self, args):
        name=args[0]
        word=args[1]
        amount=int(args[2])
        word_vectors = KeyedVectors.load(os.path.join(self.model, name))
        sim=word_vectors.most_similar(word)
        sim_amount=sim[: amount]
        print('most similar', sim_amount)
        return 0 

    def __repr__(self):
        return """Most similar words from article 
        (usage: <args> -> <name saved article model> <word> <num words out>)"""


class W2vSimilarIntellect(Command):
    def __init__(self):
       self.model=os.path.join(os.path.dirname(sys.executable), '..', word2vec_model_save_folder)
    def execute(self, args=[]):
        inn=input('quastion>')
        inn=inn.strip().lower().split()[-2]
        name=inn+'.vks'
        word=inn
        amount=10
        word_vectors = KeyedVectors.load(os.path.join(self.model, name))
        sim=word_vectors.most_similar(word)
        sim_amount=sim[: amount]
        for word in sim_amount:
            print(word[0], end=', ')
        print()    
        return 0 

    def __repr__(self):
        return """Ask what is <article name (without extension)> ?""" 

cmds = {
     'pt': PrintArticleTokenize(), 'ms': GemsimW2vSimilarWords(), 'intel': W2vSimilarIntellect()
     }

shell.set_cmd(cmds)

shell.loop()
