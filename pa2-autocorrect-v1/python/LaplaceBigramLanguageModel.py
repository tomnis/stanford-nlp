import math, collections

class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # track the vocabulary
    self.words = set([])
    # map unigrams to their raw counts
    self.unicounts = {}
    # map bigrams to their raw counts
    self.bicounts = {}
    # map bigrams to their probabilities
    self.probs = {}
    if isinstance (corpus, list):
      self.smoothval = 0
      self.train(corpus[0])
    else:
      self.smoothval = 1
      self.train(corpus)

  # track the raw counts of unigrams (necessary for conditional probability)
  def update_unicount(self, word):
    if word in self.unicounts:
      self.unicounts[word] += 1
    else:
      self.unicounts[word] = 1
  
  # track the raw counts of bigrams
  def update_bicount(self, (word1, word2)):
    if (word1, word2) in self.bicounts:
      self.bicounts[(word1, word2)] += 1
    else:
      self.bicounts[(word1, word2)] = 1

  # simply return the number of times we observed this tuple in the corpus
  def get_bicount(self, (word1, word2)):
    return self.bicounts[(word1, word2)] if (word1, word2) in self.bicounts else 0

  # use the raw counts to compute add-1 smoothed unigram probabilities
  def compute_probs(self):
    for (word1, word2) in self.bicounts:
      #print (word1, word2)
      prob = self.normalize((word1, word2))
      assert prob >= 0.0 and prob <= 1.0, "invalid probability: %f" % prob
      self.probs[(word1, word2)] = prob

  # P(word2 | word1) = (count((word1, word2)) + 1) / (count(word1) + |vocabulary|)
  def normalize(self, (word1, word2)):
    # how many times did we see <word1 word2>?
    w1w2count = self.get_bicount((word1, word2))
    # how many times did we see word1?
    w1count = self.unicounts[word1] if word1 in self.unicounts else 0
    return (w1w2count + self.smoothval) * 1.0 / (w1count + len(self.unicounts))

  # should treat a (word1, word2) not in the corpus as if it was seen once
  # P(word2 | word1) = count((word1, word2)) / count(word1)
  def get_prob(self, (word1, word2)):
    if (word1, word2) in self.probs:
      return self.probs[(word1, word2)]
    else:
      prob = self.normalize((word1, word2))
      self.probs[(word1, word2)] = prob
      return prob
  
  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      word1 = sentence.data[0].word
      # add to vocabulary
      self.words.add(word1)
      # update the unigram count
      self.update_unicount(word1)
      
      # chop off the first word
      for datum in sentence.data[1:len(sentence.data)]:
        word2 = datum.word
        # add to vocabulary
        self.words.add(word2)
        # update unigram count
        self.update_unicount(word2)
        # update bigram count
        self.update_bicount((word1, word2))
        word1 = word2

    self.compute_probs()

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    return sum(map(lambda i: math.log(self.get_prob((sentence[i-1], sentence[i]))), range(1, len(sentence)))) 
