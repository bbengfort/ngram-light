# nlp.homework1.counting
#
# Author:    Benjamin Bengfort <benben1@umbc.edu>
# Date:      Tue Oct 3 10:55:13 2012 -0400
# Objective: Submission as Homework 1 for CS 5263
#
# ID: counting.py [1] benjamin@bengfort.com $

"""
Helper data structures for use in Homework 1
"""

class Frequency(dict):
    """
    Wraps a hash map for calculating frequencies and counting.
    """

    def __setitem__(self, key, val):
        """
        Only allows integers to be set on the dictionary, raises a 
        C{ValueError} if some other type attempts to be set on it.
        """
        if not isinstance(val, int):
            raise ValueError("Set only frequency data as integers")
        super(Frequency, self).__setitem__(key,val)

    def increment(self, key):
        if key in self:
            self[key] += 1
        else:
            self[key] = 1
    incr = increment

    def decrement(self, key):
        if key in self:
            self[key] -= 1
        else:
            self[key] = 0
    decr = decrement

    def maximum(self):
        key = max(self, key=self.get)
        return key, self[key]

    def minimum(self):
        key = min(self, key=self.get)
        return key, self[key]

    def average(self):
        return sum(self.values()) / len(self)
    mean = average

    def total(self):
        """
        Returns the total counts added to the frequency.
        """
        return sum([val for val in self.values()])
