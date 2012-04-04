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
    cstar = (wcount + 1) * self.get_metacount(wcount + 1) * 1.0 / self.get_metacount(wcount)
    assert cstar != 0.0, "cstar is 0. word: %s word_count: %d N_{c+1}: %d" % (word, wcount, self.get_metacount(wcount + 1))
    return cstar

  def get_prob(self, word):
    return self.probs[word] if word in self.probs else self.normalize(word)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      for datum in sentence.data:
        word = datum.word
        self.update_count(word)

    self.compute_metacounts()
    print self.metacounts
    self.compute_probs()

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    return sum(map(lambda token: math.log(self.get_prob(token)), sentence))
