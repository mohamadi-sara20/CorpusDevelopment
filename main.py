import os
import re

import corpus_utils
import normalizer
import tagExtraction
import Ngram
import Skipgram
import zipf
import hashTags


rawPath = "/Users/macbook/Documents/sara/corpus/raw-files/"
corpusPath = "/Users/macbook/Documents/sara/corpus/processed/"
corpusFile = "body.txt"
frequencyFileName = "frequencies.txt"
lexiconFileName = "lexicon.txt"
oovCorpusFileName = "noOOV.txt"
tagsFileName = 'posTags.txt'
bigramFilename = 'bigrams.txt'
trigramFileName = 'trigrams.txt'
noStopwordFile = 'no_stopwords.txt'



#normalizer.normalize_instagram_file(rawPath, corpusPath)
#corpus_utils.separate_tags_body_in_files(corpusPath)

for fld in os.listdir(corpusPath):
    if not os.path.isdir(corpusPath + fld):
        continue
    print("Processing text collection: " + fld)
    root = corpusPath + fld + '/'
    for file in os.listdir(root):
        if not os.path.isfile(root + file) or not re.match(corpusFile, file):
            continue
        # corpus_utils.fix_words(root)
        # corpus_utils.CountWordsFile(root, corpusFile, frequencyFileName)
        # corpus_utils.selectLexicon(root, frequencyFileName, lexiconFileName)
        # corpus_utils.replaceOOV(root, corpusFile, lexiconFileName, "خاو", oovCorpusFileName)
        #
        # tagExtraction.findCategoryDistribution(root, oovCorpusFileName, tagsFileName)
        # Ngram.makeBigrams(root, corpusFile, bigramFilename)
        # Ngram.makeTrigrams(root, corpusFile, trigramFileName)
        # Skipgram.create_all_skipgrams(root, corpusFile)
        #
        # corpus_utils.filterStopwords(root)

        #zipf.create_plot(root, fld.title())

        #hashTags.remove_duplicates(root)
        #hashTags.make_frequency(root)
        word_list, matrix = hashTags.make_cooccurrence(root)
        hashTags.make_graph(word_list, matrix)