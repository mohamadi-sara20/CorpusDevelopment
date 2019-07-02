import operator
import ngram
from nltk import ngrams
from hazm import *
import nltk
from itertools import chain, combinations
import re
import os


def make_directory(out_path):
    if not os.path.exists(out_path):
        os.makedirs(out_path)

def separate_tags_body_in_post(post):
    tags = []
    body = ''
    in_body = False
    lines = post.split('\n')
    tag = False
    for line in reversed(lines):
        line = line.strip()
        if len(line) == 0:
            continue
        is_hash_tag = re.match('^[^ا-ی]*(#\S*)[^ا-ی]*$', line)
        if is_hash_tag:
            line = is_hash_tag.group(1)
            tags.append(line)
        else:
            if not in_body:
                if len(line.split()) > 2:
                    in_body = True

        if in_body:
            line = line.replace('#', '').replace('_', ' ')
            line = line.strip()
            if is_hash_tag:
                body = line + ' ' + body
                tag = True
            else:
                if tag:
                    body = line + ' ' + body
                    tag = False
                else:
                    body = line + '\n' + body
    body = body.replace('\s+', ' ').strip()
    return body, tags


def separate_tags_body_in_files(in_path):
    dirs = [in_path]
    for f in  os.listdir(in_path):
        if os.path.isdir(in_path + f):
            dirs.append('{}{}/'.format(in_path, f))

    for path in dirs:
        for f_name in os.listdir(path):
            if not f_name.endswith('normalized.txt'):
                continue
            input_file = open(path +f_name, "r", encoding="UTF8")
            body_file = open(path +f_name.replace('normalized', 'body_dup'), "w", encoding="UTF8")
            tags_file = open(path +f_name.replace('normalized', 'tags'), "w", encoding="UTF8")

            content = input_file.read()
            posts = content.split("<instagram_post>")
            for post in posts:
                body, tags = separate_tags_body_in_post(post)
                body_file.write(body+'\n')
                tags_file.write(' '.join(tags) + '\n<instagram_post>\n')


def CountWordsFile(root, corpusFilename, frequencyFileName):
    freq = {}
    c = 0
    print("Count Words in Files")
    for line in open(root + corpusFilename, encoding="UTF8"):
        line = line.strip()
        for word in line.split(' '):
            freq[word] = freq.get(word, 0) + 1
        c+=1
        if c % 1000000 == 0:
            print("Count word in progress ", c)

    print("Sort Started")
    sorted_freq = sorted(freq.items(), key=operator.itemgetter(1))
    sorted_freq.reverse()
    print("Sort Ended")

    f = open(root + frequencyFileName, "w+", encoding="UTF8")

    for word, frequency in sorted_freq:
        if frequency < 3:
            break
        else:
            f.write(word + "\t" + str(frequency)+"\n")


def selectLexicon(root, freqFilename, lexiconFileName):
    print("SelectLexicon")

    with open(root + freqFilename, encoding="UTF8") as f:
        Content = f.read().split("\n")
        # words = [word1\tfrequency1 \n word2\tfrequency2 \n ...]

    L = open(root + lexiconFileName, "w+", encoding="UTF8")
    for item in Content:
        item = item.split("\t")
        L.write(item[0]+"\n")


def replaceOOV(root, corpus_fle, lexicon_file, oovPhrase, oovCorpusFile):
    print("Replace OOV")
    with open(root + lexicon_file, encoding="UTF8") as f:
        lexicon = f.read().split("\n")

    vocab = {}
    for word in lexicon:
        vocab[word] = 1

    NoOOV = open(root + oovCorpusFile, "w+", encoding="UTF8")
    c = 0
    for Line in open(root + corpus_fle, encoding="UTF8"):
        Line = Line.split()
        LineNoOOV = ""
        for word in Line:
            if word in vocab:
                LineNoOOV += word + " "

            else:
                LineNoOOV += oovPhrase + " "

        LineNoOOV = LineNoOOV.strip()
        NoOOV.write(LineNoOOV + "\n")
        c += 1
        if c % 100000 == 0:
            print("Replace OOV Progress: ", c)

def sortFile(fileName):
    dict = {}
    for line in open(fileName, 'r'):
        if len(line.strip()) == 0:
            continue
        (key, value) = line.split('\t')
        dict[key] = value

    print("Sort Started")
    sorted_freq = sorted(dict.items(), key=operator.itemgetter(1))
    sorted_freq.reverse()
    print("Sort Ended")

    f = open(fileName, "w+", encoding="UTF8")

    for word, frequency in sorted_freq:
        f.write(word + "\t" + str(frequency))

def filterStopwords(path):
    files = ['bigrams.txt', 'frequencies.txt', 'trigrams.txt', 'skip_2_1.txt', 'skip_3_1.txt', 'skip_3_2.txt']
    stopwords = open('stopword_regex.txt', 'r').read().strip()


    for file in files:
        print(file)

        if file == 'frequencies.txt':
            pattern = "^({})\t.*".format(stopwords)
        else:
            pattern = "^.*'({})'.*".format(stopwords)
        result = ''
        for line in open(path+file, 'r'):
            if re.match(".*\'\'|^\t.*", line):
                continue
            if re.match('.*[a-zA-Z0-9۰-۹\d]+.*\t.*', line):
                continue
            if not re.match(pattern, line):
                result += line
        open(path+file+'_filtered.txt', "w+").write(result)

def fix_words(root):
    print('Fixing words >>>>>>>')
    input = open(root+'body.txt', 'r').read()
    input  = input.replace(' سپا ', ' سپاه ')
    input = input.replace(' توصی ', ' توصیه ')

    open(root + 'body.txt', 'w').write(input)

def add_rank_to_freqs(root):
    output = open(root+'frequencies_withrank.txt', 'w+')
    counter = 1
    for line in open(root+'frequencies.txt_filtered.txt', 'r'):
        output.write("{}\t{}".format(counter, line))
        counter += 1