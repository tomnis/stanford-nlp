import math, collections

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.words = set([])
    # map words to their counts
    self.counts = {}
    # map words to their unigram probabilities
    self.probs = {}
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus: # iterate over sentences in the corpus
      for datum in sentence.data: # iterate over datums in the sentence
        word = datum.word # get the word
        self.words.add(word)
        self.update_count(word)
    
    self.smooth()

  # track the raw counts of unigrams
  def update_count(self, word):
    if word in self.counts:
      self.counts[word] += 1
    else:
      self.counts[word] = 1

  # use the raw counts to compute add-1 smoothed unigram probabilities
  def smooth(self):
    for word in self.counts:
      self.probs[word] = (self.counts[word] + 1.0) / len(self.words)

  # should treat a word not in the corpus as if it was seen once
  def get_prob(self, word):
    return self.probs[word] if word in self.probs else 1.0 / len(self.words)

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    for token in sentence: # iterate over words in the sentence
      score += math.log(self.get_prob(token))
    # NOTE: a simpler method would be just score = sentence.size() * - Math.log(words.size()).
    # we show the 'for' loop for insructive purposes.
    return score
