# nlp.homework1.ngram
#
# Author:    Benjamin Bengfort <benben1@umbc.edu>
# Date:      Tue Oct 3 10:46:32 2012 -0400
# Objective: Submission as Homework 1 for CS 5263
#
# ID: ngram.py [1] benjamin@bengfort.com $

"""
Calculates the number of unigrams and bigrams (or any N-grams) in a 
corpus by using the CorpusNavigator class to go through all texts to get
indvidual words, then creats an N-Gram from them.
"""

import os
from reader import BrownNavigator, PotterNavigator
from counting import Frequency

BROWN_CORPUS  = BrownNavigator(os.environ['BROWN_CORPUS']) 
POTTER_CORPUS = PotterNavigator(os.environ['POTTER_CORPUS'])

class NGramCounter(object):
    """
    Takes as input a corpus, and then updates an internal frequency with
    word counts from the corpus.
    """

    def __init__(self, corpus, N=1):
        self.corpus = corpus
        self.frequency = Frequency()
        self.N = N

    def words(self):
        """
        A generator that goes through all the words in the corpus, makes
        them lowercase and (possibly) could remove punctuation or stopwords
        """
        for reader in self.corpus:
            for word in reader.words():
                word = word.strip()
                if word:
                    yield word.lower()

    def __iter__(self):
        """
        Expects a generator to return the specific ngram to save in the
        frequency counts.
        """
        if self.N == 1:
            # Special case for Unigrams
            for word in self.words(): yield word
        else:
            ngram = []
            for word in self.words():
                if len(ngram) < self.N:
                    ngram.append(word)
                if len(ngram) == self.N:
                    yield tuple(ngram)
                    ngram = ngram[1:]

    def count(self):
        if not self.frequency:
            for ngram in self:
                self.frequency.increment(ngram)
        return self.frequency

def brown_factory(N):
    """
    A factory for creating N-Gram counters on the Brown Corpus
    """
    return NGramCounter(BROWN_CORPUS, N)

def potter_factory(N):
    """
    A factory for creating N-Gram counters on the Harry Potter Corpus
    """
    return NGramCounter(POTTER_CORPUS, N)

brown_unigrams = brown_factory(1)
brown_bigrams  = brown_factory(2)
brown_trigrams = brown_factory(3)

potter_unigrams = potter_factory(1)
potter_bigrams  = potter_factory(2)
potter_trigrams = potter_factory(3)

if __name__ == "__main__":
    
    for envvar in ('BROWN_CORPUS', 'POTTER_CORPUS'):
        if envvar not in os.environ:
            print "Ensure that the path to the corpus is set in %s" % envvar
