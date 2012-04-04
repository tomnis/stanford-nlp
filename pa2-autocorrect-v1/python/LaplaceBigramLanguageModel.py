class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # track the vocabulary
    self.words = set([])
    # map unigrams to their raw counts
    self.counts = {}
    # map bigrams to their raw
    # map words to their unigram probabilities
    self.probs = {}
    self.train(corpus)
  
  # track the raw counts of unigrams
  def update_count(self, (word1, word2)):
    if (word1, word2) in self.counts:
      self.counts[(word1, word2)] += 1
    else:
      self.counts[(word1, word2)] = 1

  # use the raw counts to compute add-1 smoothed unigram probabilities
  def smooth(self):
    for (word1, word2) in self.counts:
      self.probs[(word1, word2)] = (self.counts[(word1, word2)] + 1.0) / len(self.words)

  # should treat a (word1, word2) not in the corpus as if it was seen once
  def get_prob(self, (word1, word2)):
    return self.probs[(word1, word2)] if (word1, word2)in self.probs else 1.0 / len(self.words)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      word1 = sentence.data[0].word
      self.words.add(word1)
      
      # chop off the first word
      for datum in sentence.data[1:len(sentence.data)]:
        word2 = datum.word
        self.words.add(word2)
        # give bigram tuple to the update count function
        self.update_count((word1, word2))

    self.smooth()

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    return 0.0
