#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools_karkkainen_sanders import *
#from tools_karkkainen_sanders import *
from array import array as array

def removeMany(end_, m, idxEnd, _lst, _max, _top, _results):
  prevStart = -1
  while m > 0:
    n, idxStart = _lst.pop()
    end_ = _max.pop()
    if (prevStart != idxStart):
      id_ = (end_, idxEnd-idxStart+1)
      if(_results.has_key(id_) and _top > _results[id_][0]) :
        _results[id_] = (_top, idxStart)
      else :
        _results[id_] = (_top, idxStart)
      prevStart = idxStart
    m -= n
    _top -= n
  if m < 0:
    _max.append((end_[0],end_[1]-n-m))
    _lst.append((-m, idxStart))
    _top -= m
  return _lst,_max,_top,_results

class Rstr_max :

  def __init__(self) :
    self.array_suffix = []
    self.array_str = []
    self.distrib = {}
  
  def add_str(self, str_unicode) :
    self.array_str.append(str_unicode)
    id_str = len(self.array_str) - 1
    len_str = len(str_unicode)

    for i in xrange(len_str) :
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

#    n = len(global_suffix)
#    self.res = [0]*k
#    global_suffix += char_final*3

#    alphabet = [None] + sorted(set(global_suffix))
#    k = len(alphabet)
#    t = dict((c, i) for i,c in enumerate(alphabet))
#    n = len(global_suffix)
#    SA = array.array('i', [0]*(n+3))
#    global_suffix = array.array('i', [t[c] for c in global_suffix]+[0]*3)
#    kark_sort(global_suffix, SA, n, k)
#    self.res = SA
    self.res = direct_kark_sort(global_suffix)
#    s,self.res = simple_kark_sort(global_suffix)


#    kark_sort(global_suffix, self.res, k, sorted(set(global_suffix)))

  def step2_lcp(self) :
    n = len(self.res)
    c = n - len(self.array_str)

    tmp = [0]*c
    rank = array('i',tmp)
    SA = array('i',tmp)

    k = 0
    for i in xrange(len(self.array_str),n) :
      key = self.distrib[self.res[i]]
      tmp[k] = self.array_suffix[key]
      rank[key] = k
      SA[k] = key
      k += 1

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
    self.SA = SA

  def step3_rstr(self) :
    _results = {}
    _top = 0         
    _lst = []        
    _max = []        
    
    prev_len = 0

    idx = 0
#    for current_len in self.lcp :      
    for idx in xrange(len(self.lcp)) :
      current_len = self.lcp[idx]
      su1  = self.array_suffix[idx]
      su2  = self.array_suffix[idx+1]
      end_ = max((su1[1], su1[0]+current_len), (su2[1], su2[0]+current_len)) 
      if prev_len < current_len:
        cp = current_len - prev_len
        _max.append(end_)
        _lst.append((cp, idx))
        _top += cp
      elif prev_len > current_len:
        _lst,_max,_top,_results = removeMany(end_, prev_len-current_len, idx, _lst, _max, _top, _results)
      elif _top > 0 and end_ > _max[-1]:
        _max[-1] = end_
      prev_len = current_len
#      idx += 1

    if _top > 0:
      _lst,_max,_top,_results = removeMany(len(self.lcp)+1, _top, idx+1, _lst, _max, _top, _results)

    return _results

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

#  str1 = open('Python.htm','r').read()
#  str1_unicode = unicode(str1,'utf-8','replace')[0:4000]
#  rstr = Rstr_max()
#  rstr.add_str(str1_unicode)
#  r = rstr.go()

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
