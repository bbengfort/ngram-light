# nlp.homework1.generate
#
# Author:    Benjamin Bengfort <benben1@umbc.edu>
# Date:      Tue Oct 14 21:26:24 2012 -0400
# Objective: Submission as Homework 1 for CS 5263
#
# ID: generate.py [1] benjamin@bengfort.com $

"""
From an N-Gram frequency count, generates random sentences.
"""

from __future__ import division # To allow floating point division with ease
import random

class UnigramSentenceGenerator(object):
    
    def __init__(self, frequency):
        self.counts = frequency
        self.ptable = {}
        self._total = None

    @property
    def total(self):
        """
        Caches the total number of words in the corpus, and counts them.
        """
        if not self._total:
            self._total = self.counts.total()
        return self._total

    @property
    def probability(self):
        """
        Calculates the probability of each unigram in the corpus by
        diving the unigram count with the total word frequency.
        """
        if not self.ptable:
            for k,v in self.counts.items():
                self.ptable[k] = v / self.total
        return self.ptable

    def random(self):
        """
        Selects a random word from the corpus by first selecting a random
        probability, then selecting a random word from the set of unigrams
        that matches the random probability.
        """

        def probable(s):
            """
            Finds all words in a corpus whose probabilities are within a 
            threshold of the seed probability, the arg to this function.
            """
            for k, v in self.probability.items():
                if s < v * 1000 and s > v / 1000:
                    yield k

        seed = random.random()
        # Generate a list of all the values that match the random frequency within a threshold
        vals = [p for p in probable(seed)]
        if vals:
            # Select a random word from those that have the same frequency as the seed
            return random.choice(vals)
        else:
            # Try again, no matches were found with that frequency
            return self.random()

    def sentence(self):
        """
        Randomly generates words until the end of sentence is reached.
        """
        # Cache the start of sentence object
        start = self.counts['<s>']
        del self.counts['<s>']

        sentence = []

        while True:
            if len(sentence) > 1 and sentence[-1] == "</s>":
                sentence = sentence[:-1]
                break
            sentence.append(self.random())

        self.counts['<s>'] = start

        return "<s>%s</s>" % " ".join(sentence)

class BigramSentenceGenerator(object):
    
    def __init__(self, unigrams, bigrams):
        self.unigrams = unigrams
        self.bigrams  = bigrams
        self.ptable   = {}

    @property
    def probability(self):
        """
        Calculates the probability of each bigram in the corpus by 
        dividing the bigram count with the unigram count of the preceeding
        word. E.g. prob(bigram(a,b)) = prob(b|a) = count(bigram(a,b)) / count(a)
        """
        if not self.ptable:
            for bigram, count in self.bigrams.items():
                self.ptable[bigram] = count / self.unigrams[bigram[0]]
        return self.ptable

    def random(self, prev):
        """
        Selects a random bigram from the corpus by first selecting a random 
        probability then selecting a random bigram from the set of bigrams
        that matches that random probability. 

        Unlike the unigram model, the previous bigram plays a roll in the
        bigrams that may be selected from, as the last word in the previous
        bigram must match the first word in the next bigram.
        """

        def probable(s, prev):
            """
            Finds all bigrams in a corpus whose probabilities are within a
            threshold of the seed probability.
            """
            for k, v in self.probability.items():
                if k[0] == prev[1]:
                    if s < v * 1000 and s > v / 1000:
                        yield k

        seed = random.random()
        vals = [b for b in probable(seed, prev)]
        if vals:
            return random.choice(vals)
        else:
            return self.random()

    def sentence(self):
        """
        Starts a sentence with a random bigram whose first part is <s>
        then builds the rest of the sentence with random bigrams.
        """
        sentence = [random.choice([b for b in self.bigrams if b[0] == "<s>"]),]

        while True:
            if sentence[-1][1] == "</s>":
                break
            bigram = self.random(sentence[-1])
            if bigram[0] != "<s>":
                sentence.append(bigram)

        sentence = [bigram[1] for bigram in sentence]
        return "<s>%s" % " ".join(sentence)

if __name__ == "__main__":
    
    import ngram 

    def print_sentences(sg):
        print sg.sentence()
        print sg.sentence()
        print sg.sentence()
        print

    print "Please hold on, this could take a while..."

    brown_unigrams  = ngram.brown_unigrams.count()
    print "..."
    brown_bigrams   = ngram.brown_bigrams.count()
    print "..."
    potter_unigrams = ngram.potter_unigrams.count()
    print "..."
    potter_bigrams  = ngram.potter_bigrams.count()
    print

    print "Unigram Sentences from the Brown Corpus:"
    print

    sg = UnigramSentenceGenerator(brown_unigrams)
    print_sentences(sg)
    
    print "Unigram Sentences from the Harry Potter Corpus:"
    print

    sg = UnigramSentenceGenerator(potter_unigrams)
    print_sentences(sg)

    print "Bigram Sentences from the Brown Corpus:"
    print

    sg = BigramSentenceGenerator(brown_unigrams, brown_bigrams)
    print_sentences(sg)

    print "Bigram Sentences from the Harry Potter Corpus:"
    print

    sg = BigramSentenceGenerator(potter_unigrams, potter_bigrams)
    print_sentences(sg)
