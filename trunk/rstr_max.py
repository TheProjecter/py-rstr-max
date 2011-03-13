#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools_karkkainen_sanders import *

class Stack:
  def __init__(self):
    self._results = {}
#    self._trigger = trigger
    self._top = 0
    self._lst = []
    self._max = []


  def _trigger(self, start, stop, end_):
    id_ = (end_, stop-start+1)
    self._results[id_] = (max(self._results[id_][0],self._top),start,stop) if(self._results.has_key(id_)) else (self._top, start, stop)
#    if(self._results.has_key(id_)) :
#      self._results[id_] = (max(self._results[id_][0],self.top),start,stop)
#    else :
#      self._results[id_] = (self.top, start, stop) #start stop == offset de lcp


  def pushMany(self, end_, n, idx):
    self._max.append(end_)
    self._lst.append((n, idx))
    self._top += n

  def removeMany(self, end_, m, idxEnd):
    prevStart = -1
    while m > 0:
      n, idxStart = self._lst.pop()
      end_ = self._max.pop()
      if (prevStart != idxStart):
#        self._trigger(idxStart, idxEnd, end_)
        id_ = (end_, idxEnd-idxStart+1)
        self._results[id_] = (max(self._results[id_][0],self._top),idxStart,idxEnd) if(self._results.has_key(id_)) else (self._top, idxStart, idxEnd)
        prevStart = idxStart
      m -= n
      self._top -= n
    if m < 0:
      self._max.append((end_[0],end_[1]-n-m))
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
      global_suffix += mot + char_frontier
      for _ in mot :
        self.distrib[k] = x
        x += 1
        k += 1
      k += 1

    n = len(global_suffix)
    self.res = [0]*n
    global_suffix += char_final*3
#    alphabet = sorted(set(global_suffix))

    kark_sort(global_suffix, self.res, n, sorted(set(global_suffix)))

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
    self.lcp = lcp
    self.SA = SA

  def step3_rstr(self) :

#    def fct(len_, start, stop, end_):
#      id_ = (end_, stop-start+1)
#      if(results.has_key(id_)) :
#        results[id_] = (max(results[id_][0],len_),start,stop)
#      else :
#        results[id_] = (len_, start, stop) #start stop == offset de lcp

    stack = Stack()
    prev_len = 0
    idx = 0
    results = {}
#    for idx in xrange(len(longestPrefixes)):
    for idx,current_len in enumerate(self.lcp):
#      current_len = longestPrefixes[idx]
#      offset1, _, idStr1  = self.array_suffix[idx]
#      offset2, _, idStr2  = self.array_suffix[idx+1]
      su1  = self.array_suffix[idx]
      su2  = self.array_suffix[idx+1]
      end_ = max((su1[2], su1[0]+current_len), (su2[2], su2[0]+current_len)) 
      if prev_len < current_len:
        cp = current_len - prev_len
#        stack.pushMany(end_, cp, idx)
        stack._max.append(end_)
        stack._lst.append((cp, idx))
        stack._top += cp
      elif prev_len > current_len:
        stack.removeMany(end_, prev_len-current_len, idx)
#        stack.setMax(end_)
      elif stack._top > 0 and end_ > stack._max[-1]:
        stack._max[-1] = end_
      prev_len = current_len

    stack.close(len(self.lcp)+1, idx+1)

#    1/0
#    stack.close(len(longestPrefixes), idx+1)
    return stack._results

  def go(self) :
    self.step1_sort_suffix()
    self.step2_lcp()
    r = self.step3_rstr()
    return r

if (__name__ == '__main__') :
#  str1 = "abd"
#  str1_unicode = unicode(str1,'utf-8','replace')[24:34]
  str1 = open('Python.htm','r').read()
  str1_unicode = unicode(str1,'utf-8','replace')[0:4000]
  rstr = Rstr_max()
  rstr.add_str(str1_unicode)
  r = rstr.go()

def tt() :
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
