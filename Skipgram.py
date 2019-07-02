from itertools import chain, combinations
import operator
import re


def pad_sequence(sequence, n, pad_left=False, pad_right=False, pad_symbol=None):
    if pad_left:
        sequence = chain((pad_symbol,) * (n-1), sequence)
    if pad_right:
        sequence = chain(sequence, (pad_symbol,) * (n-1))
    return sequence


def makeSkipgrams(sequence, n, k, pad_left=False, pad_right=False, pad_symbol=None):
    sequence_length = len(sequence)
    sequence = iter(sequence)
    sequence = pad_sequence(sequence, n, pad_left, pad_right, pad_symbol)

    if   sequence_length + pad_left + pad_right < k:
        raise Exception("The length of sentence + padding(s) < skip")

    if n < k:
        raise Exception("Degree of Ngrams (n) needs to be bigger than skip (k)")

    history = []
    nk = n+k

    if nk < 1:
        return
    elif nk > sequence_length:
        for ng in makeSkipgrams(list(sequence), n, k-1):
            yield ng

    while nk > 1: # Collects the first instance of n+k length history
        history.append(next(sequence))
        nk -= 1
    for item in sequence:
        history.append(item)
        current_token = history.pop(0)
        for idx in list(combinations(range(len(history)), n-1)):
            ng = [current_token]
            for _id in idx:
                ng.append(history[_id])
            yield tuple(ng)

    for ng in list(makeSkipgrams(history, n, k-1)):
        yield ng


def create_all_skipgrams(path, corpusFile):
    skip_2_1 = {}
    skip_3_2 = {}
    skip_3_1 = {}
    c = 1
    for line in open(path + corpusFile, "r"):
        c+=1
        if (c % 1000) == 0:
            print(c)
        for sentence in re.split('.;?!', line):
            sequence = line.split()
            if len(sequence) < 3:
                continue
            for i in makeSkipgrams(sequence, 2, 1):
                skip_2_1[i] = skip_2_1.get(i, 0) + 1
            for i in makeSkipgrams(sequence, 3, 1):
                skip_3_1[i] = skip_3_1.get(i, 0) + 1
            for i in makeSkipgrams(sequence, 3, 2):
                skip_3_2[i] = skip_3_2.get(i, 0) + 1

    with open(path+"skip_2_1.txt", "w") as f:
        sorted_freq = sorted(skip_2_1.items(), key=operator.itemgetter(1))
        sorted_freq.reverse()
        for key, freq in sorted_freq:
            f.write('{}\t{}\n'.format(key, freq))

    with open(path+"skip_3_1.txt", "w") as f:
        sorted_freq = sorted(skip_3_1.items(), key=operator.itemgetter(1))
        sorted_freq.reverse()
        for key, freq in sorted_freq:
            f.write('{}\t{}\n'.format(key, freq))

    with open(path+"skip_3_2.txt", "w") as f:
        sorted_freq = sorted(skip_3_2.items(), key=operator.itemgetter(1))
        sorted_freq.reverse()
        for key, freq in sorted_freq:
            f.write('{}\t{}\n'.format(key, freq))