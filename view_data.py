#count support of each author; visualize

from config import *
import matplotlib.pyplot as plt
import numpy as np

data = codecs.open(root_path+'/authors_encoded.txt','r','utf-8')
word_counts = {}  # key->author_index  value=>count_each
#totally 2440012 author
maxCounts = 0

for line in data:
    line = line.split(',')
    for word in line[0:-1]:
        word_counts[word] = word_counts.get(word,0) + 1
        if word_counts[word] > maxCounts:
            maxCounts = word_counts[word]
            maxKey = word

xMax = maxCounts
data.close()

#key->support,value=>author_count
bins = {}
for k,v in word_counts.items():
    bins[v] = bins.get(v,0) + 1

y = []
for i in range(40, 200):
    y.append(bins.get(i,0))

plt.plot(y,'-');
plt.grid()
plt.yticks(range(0,1000,100))
plt.xticks(range(0,160,20),range(40,200,20))
plt.xlabel('support')
plt.ylabel('count of authors')
plt.title('relationship between support and the count of authors')
plt.show()
