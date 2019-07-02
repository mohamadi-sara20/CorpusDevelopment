#reference: http://www.sociology-hacks.org/?p=151

import ngram
from nltk import ngrams
from bidi.algorithm import get_display
import numpy as np
import operator
import re
import os
import networkx as nx
import arabic_reshaper

tagsFile = "tags.txt"
tagsDup = "tags_dup.txt"
postSplitter = "<instagram_post>"
tagFreqFile = "tags_freq.txt"
tagRelationFile = "tags_relation.txt"
count = 100

def remove_duplicates(path):
    if not os.path.exists(path+tagsDup):
        os.system("mv {} {}".format(path + tagsFile, path + tagsDup))
        os.system("sort {} | uniq > {}".format(path+tagsDup, path+tagsFile))


def make_frequency(path):
    tags = {}
    for line in open(path+tagsFile, "r"):
        for word in line.split():
            word = word.strip()
            if re.match("#\S+", word):
                tags[word] = tags.get(word, 0) + 1

    sorted_freq = sorted(tags.items(), key=operator.itemgetter(1))
    sorted_freq.reverse()

    with open(path + tagFreqFile, "w+", encoding="UTF8") as output:
        for tag, freq in sorted_freq:
            output.write("{}\t{}\n".format(tag, freq))


def make_cooccurrence(path):
    words_rank = {}
    words = ""
    word_list = []
    c = 0
    for line in open(path + tagFreqFile, "r"):
        spl = line.split()
        words_rank[spl[0]] = c
        c += 1
        if c <= count:
            words += " " + spl[0]
            word_list.append(spl[0])
    words = words.strip()

    matrix = np.zeros((count, count))
    for line in open(path+tagsFile):
        spl = line.split()
        for word1 in spl:
            word1 = word1.strip()
            if not re.match("#\S+", word1):
                continue
            index1 = words_rank[word1]
            if index1 >= count:
                continue
            if not re.match("#\S+", word1):
                continue
            for word2 in spl:
                word2 = word2.strip()
                if not re.match("#\S+", word2):
                    continue
                if not re.match("#\S+", word2):
                    continue
                index2 = words_rank[word2]
                if index2 >= count:
                    continue
                if index1 == index2:
                    continue
                matrix[index1][index2] += 1

    with open(path +  tagRelationFile, "w+") as f:
        f.write(words+'\n')
        for i in range (0, count):
            for j in range(0, count):
                f.write(str(matrix[i][j]) + ' ')
            f.write('\n')
    return word_list, matrix

def make_graph(word_list, matrix):
    edgelist = []
    for i in range (0, count):
        for j in range(0, count):
            if matrix[i][j] > 50:
                artext1 = get_display(arabic_reshaper.reshape(word_list[i]))
                artext2 = get_display(arabic_reshaper.reshape(word_list[j]))
                edgelist.append( (artext1, artext2) )

    G = nx.Graph(edgelist)
    index = nx.betweenness_centrality(G)

    sorted_index = sorted(index.items(), key=lambda x: x[1], reverse=True)

    # Top 10 noun phrases by betweenness centrality:
    for word, centr in sorted_index[:10]:
        print(word, centr)

    import matplotlib as plt
    import numpy as np
    import matplotlib.pyplot as pl
    import pylab
    plt.rc('figure', figsize=(20, 15))
    G.remove_nodes_from([n for n in index if index[n] == .0])
    node_size = [index[n] * 10000 for n in G]
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, font_weight="heavy", font_size=20, node_size=node_size, edge_color='y', alpha=.4, linewidths=0)
    pl.show()
