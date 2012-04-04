from LaplaceBigramLanguageModel import *
from LaplaceUnigramLanguageModel import *

class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # we need a smoothed Unigram model...
    self.LUGM = LaplaceUnigramLanguageModel(corpus)
    # and an unsmoothed Bigram model (passing second param as a list turns off smoothing)
    self.LBGM = LaplaceBigramLanguageModel([corpus, 1])

  def get_prob(self, (word1, word2)):
    bigramcount = self.LBGM.get_bicount((word1, word2))
    return bigramcount * 1.0 / self.LUGM.get_count(word1) if bigramcount > 0 else 0.4 * self.LUGM.get_prob(word2)

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    return sum(map(lambda i: math.log(self.get_prob((sentence[i-1], sentence[i]))), range(1, len(sentence)))) 
