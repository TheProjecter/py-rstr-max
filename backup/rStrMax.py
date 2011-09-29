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

#def getSuffixes(_str):
#  n = len(_str)
#  return [SubString(_str, i, n-i) for i in xrange(n)]

def simple_kark_sort(s):
  n = len(s)
  SA = [0 for _ in s]
  s += unichr(1) * 3
  alpha = sorted(set(s))
  tools.kark_sort(s, SA, n, alpha)
  return SA

def getSortedSuffixes(s):
  return simple_kark_sort(s)
  #n = len(s)
  #result = []
  #return [SubString(s, v, n-v) for v in simple_kark_sort(s)]

def getLongestPrefixes(s, sortedAffixes):
  n = len(s)
  rank = [0 for i in xrange(n)]
  LCP = [0 for i in xrange(n-1)]
  for i in xrange(n):
    rank[sortedAffixes[i]] = i
  l = 0
  for j in xrange(n):
    l = max(0, l-1)
    i = rank[j]
    j2 = sortedAffixes[i-1]
    if i:
      while l + j < n and l + j2 < n and s[j+l] == s[j2+l]:
        l += 1
      LCP[i-1] = (i-1, l, max(j + l, j2 + l))
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
    self._max.append(end_)
    self._lst.append((n, idx))
    self._top += n
      
  def removeMany(self, end_, m, idxEnd):
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
    if m < 0:
      self._max.append(maxEnd-n-m)
      self._lst.append((-m, idxStart))
      self._top -= m

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

      
def getRepeatedStrings(s, sortedSuffixes, longestPrefixes):
  global cpt
  cpt = 0
  def fct(len_, start, stop, end_):
    global cpt
    #print '=>', len_, start, stop, "'%s'"%(sortedAffixes[start][:len_]), end_
    #print '  => last=%d len=%d rep=%d'%(end_, len_, stop-start+1), s[end_-len_:end_]
    cpt += 1
    id_ = (end_, stop-start+1)
    #print ' ', id_
    v = results.get(id_, 0)
    results[id_] = max(v, len_)
  stack = Stack(fct)
  prev_len = 0
  idx = 0
  results = {}
  for idx, current_len, end_ in longestPrefixes:
    #print '@@ %02d'%idx, current_len, '-'*10, s[end_-current_len:end_], stack._lst, stack._max, s[sortedSuffixes[idx+1]:]
    if prev_len < current_len:
      stack.pushMany(end_, current_len-prev_len, idx)
    elif prev_len > current_len:
      stack.removeMany(end_, prev_len-current_len, idx)
    else:
      stack.setMax(end_)
    prev_len = current_len
  stack.close(len(longestPrefixes)+1, idx+1)
  #print  stack._lst, stack._max
  #print '!!!', cpt
  return results

def test():
  s = open('Python.htm').read()
  s = unicode(s, "utf-8", 'replace')[:10000]
  
  bench = [s]
  for s in bench:
    print '<start :'
    #suffixes = getSuffixes(s)
    import time
    t= time.time()
    sortedSuffixes = getSortedSuffixes(s)
    longestPrefixes = getLongestPrefixes(s, sortedSuffixes)
    results = getRepeatedStrings(s, sortedSuffixes, longestPrefixes)
    print len(s), '->', time.time() - t
    print len(results)
    #print repr(s)
    #print sortedSuffixes
    #print longestPrefixes
    #print s
    for ((end, nb), l) in results.iteritems():
      ss = s[end-l:end]#SubString(s, end-l, l) #), '*', nb, ',',
      #ss = unicode(ss, 'utf8', 'replace')
      #print '***', ss, nb
      idx = 0
      try: 
        for i in xrange(nb):
          idx = s.index(ss, idx) + 1
      except ValueError, e:
        print "+++", ss, end, i, nb
      try:
        idx = s.index(ss, idx) + 1
        print "***", ss, end, i, nb
      except ValueError, e:
        pass
    #print 
    print '>stop'


if __name__ == '__main__':
  test()
