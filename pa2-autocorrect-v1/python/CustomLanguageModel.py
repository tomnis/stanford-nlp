import math, collections

class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # map unigrams to their counts
    self.counts = {}
    # map unigram counts to their counts
    self.metacounts = {}
    # map unigrams to their Good-Turing probabilities
    self.probs = {}
    self.avg_count_ratio = 0.0
    self.debug = True
    self.train(corpus)
    
  
  # track the raw counts of unigrams
  def update_count(self, word):
    if word in self.counts:
      self.counts[word] += 1
    else:
      self.counts[word] = 1
  
  # simply return the number of times we observed word in the corpus
  def get_count(self, word):
    return self.counts[word] if word in self.counts else 0

  # update the number of things that occurred count times
  def update_metacount(self, count):
    if count in self.metacounts:
      self.metacounts[count] += 1
    else:
      self.metacounts[count] = 1

  # simply return the number of words that occurred count times
  def get_metacount(self, count):
    return self.metacounts[count] if count in self.metacounts else 0

  def get_approx_metacount(self, count):
    if (self.debug):
      print "approx_metacount for %d: %d" % (count, self.get_metacount(1) * 1.0 / self.avg_count_ratio**(count -1))
    return self.get_metacount(1) * 1.0 / self.avg_count_ratio**(count -1)

  # compute the count counts
  def compute_metacounts(self):
    for word in self.counts:
      self.update_metacount(self.counts[word])

  # use the raw counts to compute Good-Turing unigram probabilities
  def compute_probs(self):
    for word in self.counts:
      self.probs[word] = self.normalize(word)
  
  # c* = (c + 1) * N_{c+1} / N_{c}
  def normalize(self, word):
    wcount = self.get_count(word)
    cstar = (wcount + 1) * self.get_approx_metacount(wcount + 1) * 1.0 / self.get_approx_metacount(wcount)
    assert cstar != 0.0, "cstar is 0. word: %s word_count: %d N_{c+1}: %d" % (word, wcount, self.get_metacount(wcount + 1))
    return cstar

  def get_prob(self, word):
    return self.probs[word] if word in self.probs else self.normalize(word)

  def find_min_zero(self):
    i = 1
    while self.get_metacount(i) > 0:
      i = i + 1
    return i
  
  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      for datum in sentence.data:
        word = datum.word
        self.update_count(word)

    self.compute_metacounts()

    print self.find_min_zero()

    i1 = self.get_metacount(1)
    ratios = []
    for k in sorted(self.metacounts.keys())[1:10]:
      #print k
      i2 = self.get_metacount(k)
      r = 1.0 * i1 / i2
      ratios.append(r)
      i1 = i2
    print ratios
    self.avg_count_ratio = sum(ratios) / len(ratios)
    
    for key in sorted(self.metacounts.keys()):
        print "f(%d) = %d    g(%d) = %d" % (key, self.get_metacount(key), key, self.get_approx_metacount(key))
    
    print self.avg_count_ratio
    
    print self.avg_count_ratio
    self.compute_probs()
    self.debug = False

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    return sum(map(lambda token: math.log(self.get_prob(token)), sentence))
