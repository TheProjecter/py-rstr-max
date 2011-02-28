# -*- coding: utf-8 -*-
import tools_karkkainen_sanders as tools

class SubString:
  def __init__(self, _str, start, length, direction=1):
    self._str = _str
    self._start = start
    self._length = length
    self._direction = 1 if direction > 0 else -1

  def __str__(self):
    return self._str[self._start:self._start+self._length*self._direction:self._direction]

  def __repr__(self):
    return '"%s"'%self
  
  def __getitem__(self, idx):
    return self._str[self._start+idx*self._direction]

  def __len__(self):
    return self._length

  def __getslice__(self, i, j):
    return SubString(self._str, self._start+i, j-i)

  def __hash__(self):
    return id(self._str) + self._start

  def __cmp__(self, other):
    minLength = min(len(self), len(other))
    for i in xrange(minLength):
      r = cmp(self[i], other[i])
      if r != 0:
        return r
    return cmp(len(self), len(other))

def pick(s):
  return iter(s).next()

def getSuffixes(_str):
  n = len(_str)
  return [SubString(_str, i, n-i) for i in xrange(n)]

def simple_kark_sort(s):
  n = len(s)
  SA = [0 for _ in s]
  s += unichr(1) * 3
  alpha = sorted(set(s))
  tools.kark_sort(s, SA, n, alpha)
  return SA

def getSortedSuffixes(suffixes):
  s = str(suffixes[0])
  n = len(s)
  result = []
  return [SubString(s, v, n-v) for v in simple_kark_sort(s)]
  return sorted(suffixes)

def getLongestPrefixes(affixes, sortedAffixes):
  n = len(affixes)
  rank = [0 for i in xrange(n)]
  LCP = [0 for i in xrange(n-1)]
  for i in xrange(n):
    rank[sortedAffixes[i]._start] = i
  l = 0
  for j in affixes:
    l = max(0, l-1)
    i = rank[j._start]
    j2 = sortedAffixes[i-1]
    if i:
      while l < len(j) and l < len(j2) and j[l] == j2[l]:
        l += 1
      LCP[i-1] = (i-1, l, max(j._start + l, j2._start + l))
    else:
      l = 0
  return LCP


class Stack:
  def __init__(self, trigger):
    self._trigger = trigger
    self._top = 0
    self._lst = []
    self._max = []

  def pushMany(self, end_, n, idx):
    #print '++', n, idx
    self._max.append(end_)
    self._lst.append((n, idx))
    self._top += n
      
  def removeMany(self, end_, m, idxEnd):
    #print '--', m, idxEnd
    prevStart = -1
    maxEnd = end_
    while m > 0:
      n, idxStart = self._lst.pop()
      maxEnd = self._max.pop()
      if (prevStart != idxStart):
        self._trigger(self._top, idxStart, idxEnd, maxEnd)
        prevStart = idxStart
      m -= n
      self._top -= n
    #print '//', m
    if m < 0:
      self._max.append(maxEnd)
      self._lst.append((-m, idxStart))
      self._top -= m
    #print '**', self._lst

  def setMax(self, value):
    #print '==', value
    if self._top <= 0:
      return
    if value > self._max[-1]:
      self._max[-1] = value
    
  def close(self, end_, idx):
    if self._top <= 0:
      return
    self.removeMany(end_, self._top, idx)

      
def getRepeatedStrings(sortedAffixes, longestPrefixes):
  results = {}
  def fct(len_, start, stop, end_):
    #print '=>', len_, start, stop, "'%s'"%(sortedAffixes[start][:len_]), end_
    #print '  last=%d len=%d rep=%d'%(end_, len_, stop-start+1)
    id_ = (end_, stop-start+1)
    v = results.get(id_, 0)
    results[id_] = max(v, len_)
  stack = Stack(fct)
  prev = sortedAffixes[0]
  prev_len = 0
  idx = 0
  for idx, current_len, end_ in longestPrefixes:
    if prev_len < current_len:
      stack.pushMany(end_, current_len-prev_len, idx)
    elif prev_len > current_len:
      stack.removeMany(end_, prev_len-current_len, idx)
    else:
      stack.setMax(end_)
    #print '@@ %02d'%idx, list(str(sortedAffixes[idx][:current_len])), stack._lst, stack._max, stack._top
    prev_len = current_len
  stack.close(len(sortedAffixes), idx+1)
  return results

def test():
  bench = [
    'totor',
    'zorro',
    'azerty'*2 + 'z',
    'aazaz',
    'azazz',
    '1234561234561234121123456123',
    'aaaa',
    'bbaaabb',
    'baaab',
    #'azerty',
    'je suis content que ca fonctionne',
    ]
  bench = ['a'*(2**i+8) for i in xrange(20)]
  #bench = ["totortoto"]
  for s in bench:
    print '<start :'
    suffixes = getSuffixes(s)
    import time
    t= time.time()
    sortedSuffixes = getSortedSuffixes(suffixes)
    longestPrefixes = getLongestPrefixes(suffixes, sortedSuffixes)
    results = getRepeatedStrings(sortedSuffixes, longestPrefixes)
    print len(s), '->', time.time() - t 
    #print repr(s)
    #print sortedSuffixes
    #print longestPrefixes
    #for ((end, nb), l) in results.iteritems():
    #  print repr(SubString(s, end-l, l)), '*', nb, ',',
    #print 
    print '>stop'

def main():
  try:
    test()
    #unittest.main()
  except SystemExit, e:
    pass

import unittest

class TestLongestPrefix(unittest.TestCase):
  def test_longestPrefix(self):
    self.assertEqual(longestPrefix('toto', 'tota'), 3)
    self.assertEqual(longestPrefix('toto', ''), 0)
    self.assertEqual(longestPrefix('toto', 'ta'), 1)    
    self.assertEqual(longestPrefix('toto', 'otota'), 0)
    self.assertEqual(longestPrefix('toto', 'toto'), 4)

class TestSubString(unittest.TestCase):

  def test_str(self):
    testStr = 'azerty'
    subString = SubString(testStr, 2, 2)
    self.assertEqual(str(subString), 'er')
    subString = SubString(testStr, 2, 2, -1)
    self.assertEqual(str(subString), 'ez')

  def test_getitem(self):
    testStr = 'azerty'
    subString = SubString(testStr, 2, 2)
    self.assertEqual(subString[3], 'y')
    subString = SubString(testStr, 2, 2, -1)
    self.assertEqual(subString[1], 'z')

  def test_cmp(self):
    testStr = 'azerty'
    s = SubString(testStr, 2, 2)
    t = SubString(testStr, 2, 2, -1)
    self.assertTrue(t > s)
    self.assertTrue(s < t)
    self.assertTrue(s != t)
    s = SubString(testStr, 2, 2)
    t = SubString(testStr, 2, 5)
    self.assertTrue(t > s)
    self.assertTrue(s < t)
    self.assertTrue(s != t)

  def test_eq(self):
    testStr = 'azertyazerty'
    s = SubString(testStr, 0, 6)
    t = SubString(testStr, 6, 6)
    self.assertTrue(t == s)
    self.assertTrue(not s<t)
    self.assertTrue(not s>t)
    self.assertTrue(not s != t)
    testStr = 'azertyytreza'
    s = SubString(testStr, 0, 6)
    t = SubString(testStr, 11, 6, -1)
    self.assertTrue(t == s)
    self.assertTrue(not s<t)
    self.assertTrue(not s>t)
    self.assertTrue(not s != t)


if __name__ == '__main__':
  main()

##def x(i, j):
##  print '=>', i, j
##
##print '-------------'
##s = Stack(x)
##print 0, s._lst
##s.pushMany(4, 7)
##print 1, s._lst
##s.addAll(10)
##print 2, s._lst
##s.removeMany(3)
##print 3, s._lst
##s.addAll(11)
##print 4, s._lst
##print '*'
##s.pushMany(1, 2)
##print 5, s._lst
##s.addAll(12)
##print 6, s._lst
##s.removeMany(2)
##print 7, s._lst
##s.addAll(13)
##print 8, s._lst
##s.pushMany(1, 5)
##print 9, s._lst
##s.close()
##print 0, s._lst
##print '+++++++++++++'
