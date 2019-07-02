import ngram
from nltk import ngrams
import operator
import re


def makeBigrams(path, corpusFilename, bigramFilename):
    twoWordCollocations = {}
    with open(path+corpusFilename) as f:
        text = f.read()
        bigrams = ngrams(text.split(), 2)
        for bigram in bigrams:
            twoWordCollocations[bigram] = twoWordCollocations.get(bigram, 0) + 1

    sorted_freq = sorted(twoWordCollocations.items(), key=operator.itemgetter(1))
    sorted_freq.reverse()

    with open(path + bigramFilename, "w+", encoding="UTF8") as output:
        for tag, freq in sorted_freq:
            output.write("{}\t{}\n".format(tag, freq))


def makeTrigrams(path, corpushFileName, trigramFileName):
    threeWordCollocations = {}
    with open(path+corpushFileName) as f:
        text = f.read()
        trigrams = ngrams(text.split(), 3)
        for trigram in trigrams:
            threeWordCollocations[trigram] = threeWordCollocations.get(trigram, 0) + 1

    sorted_freq = sorted(threeWordCollocations.items(), key=operator.itemgetter(1))
    sorted_freq.reverse()

    with open(path + trigramFileName, "w+", encoding="UTF8") as output:
        for tag, freq in sorted_freq:
            output.write("{}\t{}\n".format(tag, freq))
