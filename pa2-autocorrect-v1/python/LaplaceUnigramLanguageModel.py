import math, collections

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.words = set([])
    # map words to their counts
    self.counts = {}
    # map words to their unigram probabilities
    self.probs = {}
    if isinstance(corpus, list):
      self.smoothval = 0
      self.train(corpus[0])
    else:
      self.smoothval = 1
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

  # use the raw counts to compute add-1 smoothed unigram probabilities
  def compute_probs(self):
    for word in self.counts:
      self.probs[word] = self.normalize(word)

  def normalize(self, word):
    return (self.get_count(word) + self.smoothval) * 1.0 / len(self.words)

  # should treat a word not in the corpus as if it was seen once
  def get_prob(self, word):
    return self.probs[word] if word in self.probs else self.normalize(word)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus: # iterate over sentences in the corpus
      for datum in sentence.data: # iterate over datums in the sentence
        word = datum.word # get the word
        self.words.add(word)
        self.update_count(word)
    
    self.compute_probs()
    
  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    return sum(map(lambda token: math.log(self.get_prob(token)), sentence))
