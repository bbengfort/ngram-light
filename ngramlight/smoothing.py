# nlp.homework1.smoothing
#
# Author:    Benjamin Bengfort <benben1@umbc.edu>
# Date:      Tue Oct 15 15:17:56 2012 -0400
# Objective: Submission as Homework 1 for CS 5263
#
# ID: smoothing.py [1] benjamin@bengfort.com $

"""
Implements Good-Turing discounting on a set of bigrams and unigrams. 
"""
from __future__ import division
from generate import BigramSentenceGenerator

class GoodTuringDiscounter(BigramSentenceGenerator):
    """
    Recalculates the N-Gram counts based on the Good Turing discounting
    algorithm, by first expanding the counts to include all unseen bigrams
    in the corpora (matching all unigrams in the corpora with each other)
    then applying the GoodTuring Formula to modify the counts as follows:

    C* = (c+1) Nc+1 / Nc
    """

    def __init__(self, *args, **kwargs):
        super(GoodTuringDiscounter, self).__init__(*args, **kwargs)
        self.N = len(self.bigrams)
        self._ncounts = {}
        #self.expand()

    def expand(self):
        """
        Expands all possible bigrams in the bigram frequencies by checking
        if every unigram combination is in the bigram histogram, and if
        not, adding it as a possibility with a count of 0.
        """
        count = 0
        for unigram in self.unigrams.copy():
            for other in self.unigrams.copy():
                if (unigram, other) not in self.bigrams:
                    self.bigrams[(unigram, other)] = 0
            count += 1
            if count > 100:
                # I calcualted a rate of iteration at 1 unigram per second-
                # this means to calculate all 2474266564 bigrams possible in
                # the Brown corpus it would take 13 hours!
                break

    def countN(self, n):
        """
        Returns the count of all bigrams whose frequency is n.
        """
        if n not in self._ncounts:
            count = 0
            for frequency in self.bigrams.values():
                if frequency == n:
                    count += 1
            self._ncounts[n] = count
        return self._ncounts[n]

    def countstar(self, c):
        """
        Returns the C* for all counts whose frequency is c.
        """
        if c != 0:
            return (c+1) * (self.countN(c+1) / self.countN(c))
        else:
            return self.countN(1) / self.N

    @property
    def probability(self):
        """
        Calculates the discounted probability by dividing c* across the
        seen counts for that paritcular bigram. 
        """
        if not self.ptable:
            for bigram, count in self.bigrams.items():
                try:
                    self.ptable[bigram] = self.countstar(count) / self.unigrams[bigram[0]]
                except:
                    continue
        return self.ptable

if __name__ == "__main__":

    print "Starting"
    import ngram
    #sgb = GoodTuringDiscounter(ngram.brown_unigrams.count(), ngram.brown_bigrams.count())

    sgc = GoodTuringDiscounter(ngram.potter_unigrams.count(), ngram.potter_unigrams.count())
    print "Corpora parsed"


    #print sgb.sentence()
    #print sgc.sentence()

    #coheredb = ['he', 'went', 'quickly', 'to', 'a', 'train', 'store']
    coheredc = ['he', 'is', 'not', 'afraid', 'said', 'harry']

    for word in coheredc:
        for unigram in sgc.unigrams.copy():
            if (word, unigram) not in sgc.bigrams:
                sgc.bigrams[(word, unigram)] = 0

    print "Bigrams added"

    ptable = sgc.probability
    print "Probability calculated"


    for word in coheredc:
        for other in coheredc:
            try:
                print "%s, %s: %0.5f" % (word, other, ptable[(word,other)])
            except KeyError:
                print "%s, %s: %0.5f" % (word, other, 0.0)
