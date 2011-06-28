#Copyright (c) 2011 Yahoo! Inc. All rights reserved. Licensed under the BSD License. 
# See accompanying LICENSE file or http://www.opensource.org/licenses/BSD-3-Clause for the specific language governing permissions and limitations under the License.


""" A simple text library for normalizing, cleaning, and overlapping strings """

__author__ = "BOSS Team"

STOPWORDS = set(["I", "a", "about", "an", "are", "as", "at", "be", "by", "com", "de", "en", "for", "from",
                 "how", "in", "is", "it", "it's", "la", "of", "on", "or", "that", "the", "this", "to", "was",
                 "what", "when", "where", "who", "will", "with", "und", "the", "to", "www", "your", "you're"])

def strip_enclosed_carrots(s):
  i = s.find("<")
  if i >= 0:
    j = s.find(">", i)
    if j > i:
      j1 = j + 1
      if j1 >= len(s):
        return strip_enclosed_carrots(s[:i])
      else:
        return strip_enclosed_carrots(s[:i] + s[j1:])
  return s

def filter_stops(words):
  return filter(lambda w: w not in STOPWORDS, words) 

def uniques(s):
  return set( tokenize(s) )

def tokenize(s):
  return filter_stops(map(lambda t: t.lower().strip("\'\"`,.;-!"), s.split()))

def norm(s):
  return "".join( sorted( tokenize(s) ) )

def overlap(s1, s2):
  return len(uniques(s1) & uniques(s2))
