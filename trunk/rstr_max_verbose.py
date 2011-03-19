#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools_karkkainen_sanders import *

def does_include(s1, s2) :
  return (s1[0] + s1[1] >= s2[0] + s2[1] and s1[0] <= s2[0])

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
      self._max.append((maxEnd[0],maxEnd[1]-n-m))
      self._lst.append((-m, idxStart))
      self._top -= m

  def setMax(self, value):
    if self._top <= 0:
      return
    if value > self._max[-1]:
      self._max[-1] = value

  def close(self, end_, idx):
    if self._top <= 0:
      return
    self.removeMany(end_, self._top, idx)


class Rstr_max :

  def __init__(self) :
    self.array_suffix = []
    self.array_str = []
    self.global_equiv = []

    self.distrib_corres = []
    self.distrib = {}

  def get_suffix(self,i) :
    return self.array_suffix[i]

  def get_array_suffix(self) :
    return self.array_suffix

  def get_str(self,i) :
    return self.array_str[i] 

  def get_array_str(self,i) :
    return self.array_str
  
  def add_str(self, str_unicode) :
    self.array_str.append(str_unicode)
    id_str = len(self.array_str) - 1
    len_str = len(str_unicode)

    for i in xrange(len_str) :
      self.array_suffix.append((i, len_str-i, id_str))

  def step1_sort_suffix(self) :
    char_frontier = chr(2)
    char_final = chr(1)
    global_suffix = ''

    x = k = 0
    for mot in self.array_str :
      global_suffix += mot
      for l in mot :
        self.distrib_corres.append(k)
        self.distrib[k] = x
        k += 1
        x += 1
      global_suffix += char_frontier
      k +=1

    self.n = len(global_suffix)
    global_suffix += char_final*3

    alphabet = sorted(set(global_suffix))

    self.res = [0]*self.n
    kark_sort(global_suffix, self.res, self.n, alphabet)

  def step2_lcp(self) :
    k = 0
    n = len(self.res)
    c = n - len(self.array_str)

    rank = [0]*c
    tmp = [0]*c
    SA = [0]*c

    k = 0
    for i in xrange(n) :
      if self.distrib.has_key(self.res[i]) :
        key = self.distrib[self.res[i]]
        tmp[k] = self.array_suffix[key]
        rank[key] = k
        SA[k] = key
        k += 1

    l = 0
    lcp = [0]*(k-1)
    for j in xrange(k) :
      if(l > 0) :
        l -= 1
      if rank[j] != 0 :
        su_j   = self.array_suffix[j]
        str_j  = self.array_str[su_j[2]]
        su_jj  = self.array_suffix[SA[rank[j]-1]]
        str_jj = self.array_str[su_jj[2]]
        while(l < su_j[1] and l < su_jj[1] and str_j[l + su_j[0]] == str_jj[l + su_jj[0]]) :
          l += 1
        lcp[rank[j]-1] = l
      else :
        l = 0

    self.array_suffix = tmp

#    print self.array_suffix
#    print lcp

    self.lcp = lcp
    self.SA = SA
    return k

  def step3_rstr(self) :
    sortedSuffixes = self.SA
    longestPrefixes = self.lcp

    def fct(len_, start, stop, end_):
      id_ = (end_, stop-start+1)
      if(results.has_key(id_)) :
        if(len_ > results[id_][0]) :
          results[id_] = (max(results[id_][0],len_),start,stop)
      else :
        results[id_] = (len_, start, stop) #start stop == offset de lcp
#      print len_
#      print results

#      results[id_]
#      print "!!!",v
#      results[id_] = (max(v, len_),start, stop) #start stop == offset de lcp

    stack = Stack(fct)
    prev_len = 0
    idx = 0
    results = {}
    for idx in xrange(len(longestPrefixes)):
      current_len = longestPrefixes[idx]
      offset1, _, idStr1  = self.array_suffix[idx]
      offset2, _, idStr2  = self.array_suffix[idx+1]
      end_ = max((idStr1, offset1+current_len), (idStr2, offset2+current_len)) 
      if prev_len < current_len:
        stack.pushMany(end_, current_len-prev_len, idx)
      elif prev_len > current_len:
        stack.removeMany(end_, prev_len-current_len, idx)
      else:
        stack.setMax(end_)
      prev_len = current_len

    stack.close(len(longestPrefixes)+1, idx+1)

#    1/0
#    stack.close(len(longestPrefixes), idx+1)
    return results

  def go(self) :
    self.step1_sort_suffix()
    self.step2_lcp()
    r = self.step3_rstr()
    return r

if (__name__ == '__main__') :
  str1 = 'abd'*100000
  str1_unicode = unicode(str1,'utf-8','replace')[0:4000]
  rstr = Rstr_max()
  rstr.add_str(str1_unicode)
  rstr.add_str(str1_unicode)
  rstr.add_str(str1_unicode)
  rstr.add_str(str1_unicode)
  r = rstr.go()

def p() :
  #for ((end, nb), (l, start_plage, end_plage)) in r.iteritems():
  for ((idStr, end), nb), (l, start_plage, end_plage) in r.iteritems():
    ss = rstr.get_str(idStr)[end-l:end]
    s = rstr.get_str(idStr)
    #ss = s[end-l:end]#SubString(s, end-l, l) #), '*', nb, ',',
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



  1/0


  for ((idStr, end), nb), (l, start_plage, end_plage) in r.iteritems():
    ss = rstr.get_str(idStr)[end-l:end]
    print ss
    print l, start_plage, end_plage
    for o in range(start_plage, end_plage+1) :
      su = rstr.array_suffix[o]
      sss = rstr.array_str[su[2]][su[0]:su[0]+l]
#      print sss, su, su[0], l, su[2]

  1/0
  pass
