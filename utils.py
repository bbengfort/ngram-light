# nlp.homework1.utils
#
# Author:    Benjamin Bengfort <benben1@umbc.edu>
# Date:      Tue Oct 3 09:34:10 2012 -0400
# Objective: Submission as Homework 1 for CS 5263
#
# ID: utils.py [1] benjamin@bengfort.com $

"""
Utility classes and helper functions.
"""

import os

class Directory(object):
    """
    Emulates a directory object to ensure that the path has environment
    variables expanded, and that the directory exists and contains files.

    @note: This is an implementation of a Python Descriptor.
    """
    
    def __init__(self, fget, doc=None):
        self.fget = fget
        self.name = self.mangle(fget.__name__)
        self.__doc__ = doc
    
    def expand(self, path):
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)

        if os.path.isdir(path):
            return path
        raise ValueError("Please specify a path to an existing directory")

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, self.expand(value))

    def __delete__(self, instance):
        delattr(instance, self.name)

    def mangle(self, name):
        return "_" + self.__class__.__name__ + "__" + name

def directory(func):
    return Directory(func, func.__doc__)

class Stopwords(object):
    """
    Loads up the list of stopwords from an associated stopwords.text file
    """

    def __init__(self, path="stopwords.txt"):
        self.path = path

    def __iter__(self):
        with open(self.path, 'rb') as wordfile:
            for line in wordfile.readlines():
                line = line.strip()
                if line:
                    yield line
