# reference: https://github.com/AlxndrMlk/stochasticZipf/blob/master/Get_Zipf.ipynb
from __future__ import division
from pylab import *


def create_plot(root, subject):
    freq = []
    c = 0
    for line in open(root + 'frequencies.txt'):
        line = line.split('\t')
        freq.append(float(line[1]))
        c += float(line[1])
    values = array(freq) / c
    indexes = np.arange(len(values))

    line_x = np.arange(1, len(values))
    alpha = (-np.log(6) / np.log(5))
    line_y = (1 / sum(line_x ** alpha)) * line_x ** alpha
    plt.figure(figsize=(9.7, 6))
    plt.scatter(indexes, values, alpha=.5, label='Empirical', color="#db43ce")
    plt.plot(line_x, line_y, color='black', alpha=.3, label="Zipf's slope")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Rank")
    plt.ylabel('Frequency of occurences')
    plt.title("Zipf's slope for \"{}\" - word count: {:,}".format(subject, int(c)), fontsize='18')
    #plt.title("$n = 10,000$", alpha=.7)
    plt.legend()
    plt.show()
