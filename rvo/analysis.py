#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import nltk
import datetime
import hurry.filesize

def get_sentences(content):
    """
    Returns the number of sentences
    :content: str
    :returns: int
    """
    sentences = len(nltk.tokenize.sent_tokenize(content))
    return sentences

def get_words(content):
    """
    Returns the number of sentences
    :content: str
    :returns: int
    """
    words = len(nltk.word_tokenize(content))
    return words

def get_characters(content):
    """
    Returns the number of sentences
    :content: str
    :returns: int
    """
    characters = len(content)
    return characters

def get_word_distribution(content):
    """
    Returns a distribution file on words
    """

    # Remove non alphanumeric chars
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(content)

    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 1]

    # Remove numbers
    words = [word for word in words if not word.isnumeric()]

    # Lowercase all words (default_stopwords are lowercase too)
    words = [word.lower() for word in words]

    # Remove numbers
    words = [word for word in words if not word.isnumeric()]

    # Remove english stopwords
    words = [word for word in words if word not in nltk.corpus.stopwords.words('english')]

    # Remove german stopwords
    words = [word for word in words if word not in nltk.corpus.stopwords.words('german')]


    # Calculate frequency distribution
    fdist = nltk.FreqDist(words)

    return fdist


def get_most_common_words(content, count):
    """
    Get list of words that are most commonly
    used in this text
    :content: str
    :words: int - number of words as result
    :returns: tuple - (words,frequency)
    """
    fdist = get_word_distribution(content)
    return fdist.most_common(count)

def get_least_common_words(content, count):
    """
    Get list of words that are least commonly
    used in this text
    :content: str
    :count: int - number of words as result
    :returns: list
    """
    fdist = get_word_distribution(content)
    return fdist.hapaxes()[0:count]

def get_words_per_sentence(content):
    """
    Get words per sentance average
    :content: str
    :returns: int
    """
    words = get_words(content)
    sentences = get_sentences(content)
    return words / sentences

def get_long_words(content,count):
    """
    Get list of words that are least commonly
    used in this text
    :content: str
    :count: int - number of words as result
    :returns: list
    """
    fdist = get_word_distribution(content)
    longwords = []
    for word in fdist:
        if len(word) > 10:
            longwords.append(word)

    longwords = sorted(longwords, key=len, reverse=True)

    return longwords[0:count]

def get_age_of_document(created):
    """
    Returns the age of a document as
    string.
    :created: date
    :returns: str
    """
    today = datetime.datetime.now()
    age = today - created
    return str(age)

def get_size_of_document(content):
    """
    Returns human readable size of document
    :content: str
    :returns: str
    """
    s = sys.getsizeof(content)
    s = hurry.filesize.size(s, system=hurry.filesize.alternative)

    return s
