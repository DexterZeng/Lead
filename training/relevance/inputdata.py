import collections
import numpy as np
from scipy.stats import pearsonr

import math
import os
import random

from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
data_index = 0
class Options(object):
  def __init__(self, datafile, vocabulary_size):
    self.vocabulary_size = vocabulary_size
    self.save_path = "tmp"
    data_or, self.count, self.vocab_words = self.build_dataset(datafile,
                                                              self.vocabulary_size) 
    #self.train_data = self.subsampling(data_or)
    self.train_data = data_or

    self.sample_table = self.init_sample_table()

    self.save_vocab()


  def build_dataset(self, filename, n_words):
    ### reformulate the input!!!

    count = [['UNK', 0]] ## list''' each element is also a pair
    words = [] # store all the words
    input = open(filename, 'r')
    for line in input:
      parts = line.split('\t')
      if len(parts)!= 3: continue
      ents = parts[2].split(' ')
      query= parts[0].split(' ')
      words.extend(query)
      for ent in ents:
        name = ent.split('*')[0]
        if '/wiki/' in name:
            words.append(name)
    # reduce the vocab to a specified number
    count.extend(collections.Counter(words).most_common(n_words - 1)) ## obtain the top 100000 entities ...
    word2id = dict()
    for word, _ in count:
      word2id[word] = len(word2id)

    data = list() ## convert all the words into ids!!!! and prepare inputs
    #unk_count = 0
    input1 = open(filename, 'r')
    for line in input1:
      parts = line.split('\t')
      if len(parts)!= 3: continue
      ents = parts[2].split(' ')
      query= parts[0].split(' ')
      query_ids = []
      for q in query:
        try:
            query_ids.append(word2id[q])
        except:
            #unk_count += 1
            continue
      if len(query_ids) >=1 :
        for ent in ents:
            try:
                name = ent.split('*')[0]
                nameid = word2id[name]
                data.append([query_ids, nameid])
            except:
                #unk_count += 1
                continue
    #count[0][1] = unk_count # unknown words frequencies
    id2word = dict(zip(word2id.values(), word2id.keys()))# id2words
    return data, count, id2word # ids, frequencies, mapdic

  def save_vocab(self):
    with open(os.path.join(self.save_path, "vocab.txt"), "w") as f:
      for i in xrange(len(self.count)):
        vocab_word = self.vocab_words[i]
        f.write("%s %d\n" % (vocab_word, self.count[i][1])) 

  def init_sample_table(self):

    count = [ele[1] for ele in self.count]
    pow_frequency = np.array(count)**0.75
    power = sum(pow_frequency)
    ratio = pow_frequency/ power
    table_size = 1e8
    count = np.round(ratio*table_size)
    sample_table = []
    for idx, x in enumerate(count):
      sample_table += [idx]*int(x)
    return np.array(sample_table)

  def weight_table(self):
    count = [ele[1] for ele in self.count]
    pow_frequency = np.array(count)**0.75
    power = sum(pow_frequency)
    ratio = pow_frequency/ power
    return np.array(ratio)


  def generate_batch(self, batch_size, count):
    data = self.train_data
    global data_index
    if data_index + batch_size > len(data):
      data_index = 0
      self.process = False
    batch_data = data[data_index:data_index+batch_size]
    data_index = data_index+ batch_size
    neg_v = np.random.choice(
            self.sample_table, size=(batch_size, count)).tolist()
    return batch_data, neg_v

import json, csv
from scipy.stats import spearmanr
import math
def cosine_similarity(v1,v2):
  "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
  sumxx, sumxy, sumyy = 0, 0, 0
  for i in range(len(v1)):
    x = v1[i]; y = v2[i]
    sumxx += x*x
    sumyy += y*y
    sumxy += x*y
  return sumxy/math.sqrt(sumxx*sumyy)

def scorefunction(embed):

  f = open('./tmp/vocab.txt')
  line = f.readline()
  vocab = []
  wordindex = dict()
  index = 0
  while line:
    word = line.strip().split()[0]
    wordindex[word] = index
    index = index +1
    line = f.readline()
  f.close()
  ze = []
  input = open('./Wire.txt')
  index = 0
  consim = []
  humansim = []
  for line in input:
    strs = line.strip().split('\t')
    if index==0:
      index = 1
      continue
    if (strs[0] not in wordindex) or (strs[1] not in wordindex):
      continue

    humansim.append(float(strs[2]))


    value1 =  embed[int(wordindex[strs[0]])]
    value2 =  embed[int(wordindex[strs[1]])]
    index =index + 1
    score = cosine_similarity(value1, value2)
    consim.append(score)


  cor1, pvalue1 = spearmanr(humansim, consim)

  cor2, pvalue2 = pearsonr(humansim, consim)


  return cor1,cor2,len(humansim)
