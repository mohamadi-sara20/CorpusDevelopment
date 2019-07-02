from hazm import *
import nltk, matplotlib



class Tagger(object):
    def __init__(self):
        '''Constructor: Initializes POSTagger'''
        self.tagger = POSTagger(model='postagger.model')

    def tag_sentence(self, list_of_tokens):
        '''
        tags a sentence
        :param list_of_tokens: words of a sentence
        :param list_of_tokens type: list of str
        :return: the corresponding tags
        :rtype: list of str
        '''
        word_tag_tuples = self.tagger.tag(list_of_tokens)
        list_of_tags = [wtt[1] for wtt in word_tag_tuples]
        return list_of_tags


def findCategoryDistribution(root, corpusFile, tagsFile):
    postagger = Tagger()
    with open(root+corpusFile) as f:
        text = f.readlines()
    tags = {}
    c = 0
    for line in text:
        c += 1
        tagged_text = postagger.tag_sentence(word_tokenize(line))
        i = 0
        for tag in tagged_text:
            tags[tag] = tags.get(tag, 0) + 1

        if (c % 1000) == 0:
            print("PROGESS: {}".format(c))

    with open(root + tagsFile, "w+", encoding="UTF8") as output:
        for tag in tags.keys():
            output.write("{}\t{}\n".format(tag, tags[tag]))
