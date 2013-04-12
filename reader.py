# nlp.homework1.reader
#
# Author:    Benjamin Bengfort <benben1@umbc.edu>
# Date:      Tue Oct 2 22:04:04 2012 -0400
# Objective: Submission as Homework 1 for CS 5263
#
# ID: reader.py [1] benjamin@bengfort.com $

"""
Opens a Corpus and yields the text for reading, splitting the text into
either paragraphs, sentences, or words using a means specific to the corpus
the program is reading. 

@note: The HTML files in Harry Potter are preprocessed by an HTML DOM 
processor called BeautifulSoup.
"""

import os
import re
from utils import directory
from bs4 import BeautifulSoup

class CorpusReader(object):
    """
    A file-like object that reads every file from the corpus and exposes
    various methods for handling and manipulating the text. This is a 
    wrapper around a file object with an embedded path.
    """

    def __init__(self, abspath):
        self.path = abspath
        self.open()

    def open(self):
        """
        Opens the file on the file system.
        """
        if hasattr(self, 'text'):
            raise IOError("Must close the reader before you can open it again.")
        else:
            self.text = open(self.path, 'rb')
        return self

    def close(self):
        """
        Closes the file on the file system.
        """
        self.text.close()
        del self.text

    def read(self, *args):
        return self.text.read(*args)

    def readlines(self):
        return self.text.readlines()

    def sentences(self):
        """
        Return a generator of sentences
        """
        raise NotImplementedError()

    def paragraphs(self):
        """
        Return a generator of lists of sentences that makes up a paragraph.
        """
        raise NotImplementedError()

    def words(self):
        """
        Return a generator of words in the reader.
        """
        raise NotImplementedError()

    def __enter__(self):
        """
        A Python context manager.
        """
        return self

    def __exit__(self, type, value, tb):
        """
        A Python context manager that ensures this file is closed.
        """
        self.close()

class CorpusNavigator(object):
    """
    Expects a directory containing the contents of the corpus, it will 
    then iterate through the contents of the directory, exposing the 
    absolute path of every file in the directory for use by a Reader class
    """

    reader_class = CorpusReader

    def __init__(self, dirpath, filemask=['*'], ignoreHidden=True):
        self.root = dirpath
        self.filemask = [re.compile(f.replace('.', "[.]").replace("*", ".*").replace("?", ".")) for f in filemask]
        self.ignoreHidden = ignoreHidden

    @directory
    def root(self): pass

    @property
    def readme(self):
        """
        Searches for the readme in the root directory.
        """
        try:
            return self.abspath("README")
        except OSError:
            return None

    def isHidden(self, fname):
        if fname[0] in ('.', '~'):
            return True
        return False

    def isMasked(self, fname):
        for r in self.filemask:
            if r.match(fname):
                if self.ignoreHidden:
                    return not self.isHidden(fname)
                return True
        return False

    def abspath(self, fname):
        """
        Returns the absolute path for the given file descriptor
        """
        path = os.path.join(self.root, fname)
        if os.path.isfile(path):
            return path
        raise OSError("%s is not a valid file" % path)

    def list(self):
        """
        Lists the contents of the directory of the corpus, but will not
        walk subdirectories, and will only expose the file names. This 
        method will also check if the file is masked so you can exclude
        hidden files and files that are not part of the corpus (e.g. a 
        README file).
        """
        for name in os.listdir(self.root):
            if os.path.isfile(self.abspath(name)):
                if self.isMasked(name):
                    yield name

    def __iter__(self):
        """
        Returns an open CorpusReader object for each file that is listed.
        """
        for fname in self.list():
            with self.reader_class(self.abspath(fname)) as reader:
                yield reader

class BrownReader(CorpusReader):
    """
    A reader specifically for files in the Brown corpus, formatted for the
    C style Brown corpus documents (with part of speech tags).
    """
    
    def sentences(self):
        """
        In Brown, each sentence is a line, so return each line (and strip
        off the new line character at the end).
        """
        for line in self.readlines():
            line = line.strip()
            if line:
                yield line

    def paragraphs(self):
        """
        In Brown, paragraphs are separated by one or more blank lines.
        Sentences are each on a line by themselves.
        """
        paras = []
        for line in self.readlines():
            if line == '\n':
                if paras:
                    yield paras
                    paras = []
            else:
                paras.append(line.strip())

    def words(self):
        """
        Strips out the Brown tags and returns only the words.
        """
        for sent in self.sentences():
            yield "<s>"
            for word in sent.split():
                word = word.split('/')
                if word[0]:
                    yield word[0]
            yield "</s>"

class BrownNavigator(CorpusNavigator):
    """
    In the Brown Corpus, each line is a sentence, and each paragraph is
    separated by a double newline (\n\n). I have version C of the corpus,
    meaning that every word is also tagged with its part of speech, so
    removal is necessary.
    """

    reader_class = BrownReader
    
    def __init__(self, dirpath):
        super(BrownNavigator, self).__init__(dirpath, ["c[a-z]\d+"])

class PotterReader(CorpusReader):
    """
    A reader specifically for the html files in the Harry Potter books.
    This readers uses an external library, Beautiful Soup to quickly get
    the DOM of an HTML document and export all the paragraph tags. Its 
    only use in this library is for the quick export of HTML text into a
    format readable by the reader. 

    For sentences and words, regular expressions are used to separate the
    segments and tokens. This has obvious difficulties like punctuation,
    and single word sentences like Dr. -- but is deemed good enough for
    this application.

    @note: This Reader uses an external library, BeautifulSoup.
    @note: The copyright of the Harry Potter books belongs to Scholastic-
        I'm claiming fair use of these books, purchased through the 
        Pottermore site for Academic use only. The content of the corpora
        should not (and will not) be distributed outside the scope of 
        class participation for a homework assignment.
    """

    def paragraphs(self):
        """
        Use BeautifulSoup to extract all the paragraph tags from the text.
        """
        soup = BeautifulSoup(self)
        for p in soup.find_all('p'):
            text = p.string
            if text:
                for nl in ('\n\n', '\r\n', '\r'):
                    text = text.replace(nl, '\n')
                text = text.strip()
                text = text.replace('\n', ' ')
                if text:
                    yield text

    def sentences(self):
        """
        Use a regular expression to extract all the sentences from each
        paragraph. This regular expression was adapted from a post on
        Stack Overflow. The link to the source can be provided on request.
        """
        segmenter = re.compile(r"(\S.+?[.!?])(?=\s+|$)")
        for paragraph in self.paragraphs():
            for match in segmenter.findall(paragraph):
                yield match

    def words(self):
        """
        Use a regular expression to extract all word boundaries from the
        paragraphs. using the \b boundary can result in errors, and does
        not include punctuation, but is good enough for this application.
        """
        tokenizer = re.compile(r"(\b\w+\b)")
        for sentence in self.sentences():
            yield "<s>"
            for match in tokenizer.findall(sentence):
                yield match
            yield "</s>"

class PotterNavigator(CorpusNavigator):
    """
    Extracts all the HTML documents out of the specified directory and 
    then parses the documents with BeautifulSoup (an external HTML parser
    library). Regular Expressions are used to break out sentences and
    tokens from the text.
    """

    reader_class = PotterReader

    def __init__(self, dirpath):
        super (PotterNavigator, self).__init__(dirpath, ["*.html"])
