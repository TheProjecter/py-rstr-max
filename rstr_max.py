#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools_karkkainen_sanders import direct_kark_sort
from array import array

class Stack:
  def __init__(self, trigger):
    self._trigger = trigger
    self._top = 0
    self.lst_max = []

#  def pushMany(self, end_, n, idx):
#    self.lst_max.append([(n, idx), end_])
#    self._top += n

  def removeMany(self, end_, m, idxEnd):
    prevStart = -1
    maxEnd = end_
    while m > 0:
      (n, idxStart), maxEnd = self.lst_max.pop()
      if (prevStart != idxStart):
        self._trigger(self._top, idxStart, idxEnd, maxEnd)
        prevStart = idxStart
      m -= n
      self._top -= n
    if m < 0:
      self.lst_max.append([(-m, idxStart), (maxEnd[0],maxEnd[1]-n-m)])
      self._top -= m

#  def setMax(self, value):
#    if self._top <= 0:
#      return
#    if value > self.lst_max[-1][1] :
#      self.lst_max[-1][1] = value

#  def close(self, end_, idx):
#    if self._top <= 0:
#      return
#    self.removeMany(end_, self._top, idx)

class Rstr_max :

  def __init__(self) :
    self.array_suffix = []
    self.array_str = []
    self.global_equiv = []

    self.distrib_corres = []
    self.distrib = {}

  def add_str(self, str_unicode) :
    self.array_str.append(str_unicode)
    id_str = len(self.array_str) - 1

    for i in xrange(len(str_unicode)) :
      self.array_suffix.append((i, id_str))

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

    self.res = direct_kark_sort(global_suffix)

  def step2_lcp(self) :
    n = len(self.res)
    tmp = [0]*(n - len(self.array_str))
    rank = array('i',tmp)
    SA = array('i',tmp)

    k = 0
    for i in xrange(len(self.array_str),n) :
      key = self.distrib[self.res[i]]
      tmp[k] = self.array_suffix[key]
      rank[key] = k
      SA[k] = key
      k += 1

    self.distrib = None

    l = 0
    lcp = array('i',[0]*(k-1))
    for j in xrange(k) :
      if(l > 0) :
        l -= 1
      if rank[j] != 0 :
        su1 = self.array_suffix[j]
        str_j = self.array_str[su1[1]]
        len_j = len(str_j) - su1[0]
        su2 = self.array_suffix[SA[rank[j]-1]]
        str_jj = self.array_str[su2[1]]
        len_jj = len(str_jj) - su2[0]
        while(l < len_j and l < len_jj and str_j[l + su1[0]] == str_jj[l + su2[0]]) :
          l += 1
        lcp[rank[j]-1] = l
      else :
        l = 0

    self.array_suffix = tmp
    self.lcp = lcp
#    self.SA = SA

  def step3_rstr(self) :
    prev_len = 0
    idx = 0
    results = {}
    len_lcp = len(self.lcp)

    def fct(len_, start, stop, end_):
      id_ = (end_, stop-start+1)
      if(results.has_key(id_)) :
        if(len_ > results[id_][0]) :
          results[id_] = (max(results[id_][0],len_),start)
      else :
        results[id_] = (len_, start) #start stop == offset de lcp

    stack = Stack(fct)
    for idx in xrange(len_lcp):
      current_len = self.lcp[idx]
      offset1, idStr1  = self.array_suffix[idx]
      offset2, idStr2  = self.array_suffix[idx+1]
      end_ = max((idStr1, offset1+current_len), (idStr2, offset2+current_len)) 
      n = prev_len - current_len
      if n < 0 :
        #pushMany
        stack.lst_max.append([(-n, idx), end_])
        stack._top += -n
      elif n > 0:
        stack.removeMany(end_, n, idx)
      elif stack._top > 0 and end_ > stack.lst_max[-1][1] :
        #setMax
        stack.lst_max[-1][1] = end_

      prev_len = current_len

    if(stack._top <= 0) :
      stack.removeMany(len_lcp+1, stack._top, idx+1)

#    stack.close(len_lcp+1, idx+1)

    return results

  def go(self) :
    self.step1_sort_suffix()
    self.step2_lcp()
    r = self.step3_rstr()
    return r

if (__name__ == '__main__') :
  str1 = 'toto'
  str1_unicode = unicode(str1,'utf-8','replace')
  rstr = Rstr_max()
  rstr.add_str(str1_unicode)
  r = rstr.go()
  for ((id_str, end), nb), (l, start_plage) in r.iteritems():
    ss = rstr.array_str[id_str][end-l:end]
    print '[%s] %d'%(ss.encode('utf-8'), nb)

