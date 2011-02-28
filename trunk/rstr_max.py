#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools_karkkainen_sanders import *
from suffix_array import *
from string import *

def reverse_string(s) :
  return s[::-1]

def array_merge(a1,a2) :
  a1.extend(a2)
  return a1

def does_include(s1, s2) :
  return (s1[0] + s1[1] >= s2[0] + s2[1] and s1[0] <= s2[0])

# su = suffixe, c-a-d un couple (offset,id_str)

class Rstr_max :

  def __init__(self) :
    self.array_suffix = []
    self.array_str = []
    self.global_equiv = []
    self.global_equiv_rev = []

    self.distrib_corres = []
    self.distrib = {}
    pass

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
    for i,s in enumerate(str_unicode) :
      suffix = (i, len_str-i, id_str)
      self.array_suffix.append(suffix)

    self.global_equiv.append(str_unicode)
#    l_str_rev_unicode = [reverse_string(str_unicode)]
    l_str_rev_unicode = [str_unicode[::-1]]
    l_str_rev_unicode.extend(self.global_equiv_rev)   
#    self.global_equiv_rev = array_merge([str_rev_unicode], self.global_equiv_rev)
    self.global_equiv_rev = l_str_rev_unicode

  def step_1_sort_suffix(self) :
    caractere_frontier = chr(2)
    caractere_final = chr(1)
    global_suffix = ''

    x = k = 0
    for id_suffix,mot in enumerate(self.global_equiv) :
      global_suffix += mot
      for l in mot :
        self.distrib_corres.append(k)
        self.distrib[k] = x
        k += 1
        x += 1
      global_suffix += caractere_frontier
      k +=1

    rev = reverse_string(global_suffix)
    global_suffix_rev = rev[1:] + caractere_frontier

    self.n = len(global_suffix)
    global_suffix += caractere_final*3
    global_suffix_rev += caractere_final*3

    alphabet = lst_char(global_suffix)

    self.res = [0]*self.n
    kark_sort(global_suffix, self.res, self.n, alphabet)

    self.res_rev = [0]*self.n
    kark_sort(global_suffix_rev, self.res_rev, self.n, alphabet)

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
    lcp = [0]*(k+1)
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
      else :
        l = 0
      lcp[rank[j]] = l
    lcp[k] = 0

    self.array_suffix = tmp
    self.lcp = lcp
    self.SA = SA
    return k

  def rstr(self, b, e) :
    mini = self.lcp[b]
    mini_pos = [b]
    k = 1
    for i in xrange(b+1,e) :
      if mini > self.lcp[i] :
        mini = self.lcp[i]
        mini_pos = [i]
        k = 1 
      elif mini == self.lcp[i] :
        mini_pos.append(i)
        k += 1 

    if mini > 0 :
      pos = [i for i in xrange(b-1,e)]
      beg = self.SA[b-1]
      corres = self.n - (self.distrib_corres[beg] + mini - 1) - 2
      self.array_repeated.append(pos)
      cpt = len(self.array_repeated) - 1
      if not self.corres_su_pre.has_key(corres) :
        self.corres_su_pre[corres] = {}
      self.corres_su_pre[corres][mini] = cpt

    if k != e-b :
      ppos = b
      mini_pos.append(e)
      k += 1
      for i in xrange(k) :
        if (mini_pos[i] - ppos) > 0 :
          self.rstr(ppos, mini_pos[i])
        ppos = mini_pos[i] + 1

  def step3_rstr(self, k) :
    self.corres_su_pre = {}
    self.array_repeated = []
    self.rstr(0,k)

  def step4_rstr_max(self) :
    flag = False
    sort_list = []
    for i in xrange(self.n) :
      o = self.res_rev[i]
      if self.corres_su_pre.has_key(o) :
        l = self.corres_su_pre[o].keys()
        l.sort()
        for length in l :
          cpt = self.corres_su_pre[o][length]
          info = (length, self.array_repeated[cpt])
          su = self.array_suffix[info[1][0]]
          new_su = (su[0], length, su[2])
          if flag :
            if (len(old_info[1]) != len(info[1])) or (not does_include(new_su, old_su)) :
              sort_list.append(old_info)
          old_info = info
          old_su = new_su
          flag = True

    sort_list.append(old_info)
    self.array_repeated = sort_list

  def go(self) :
    self.step_1_sort_suffix()
    k = self.step2_lcp()
    self.step3_rstr(k)
    self.step4_rstr_max()
    return self.array_repeated

if (__name__ == '__main__') :
  str1 = 'ab'*200
  str1_unicode = unicode(str1,'utf-8','replace')
  rstr = Rstr_max()
  rstr.add_str(str1_unicode)
  rstr.add_str(str1_unicode)
  rstr.add_str(str1_unicode)

  array_repeated = rstr.go()
  print array_repeated
  pass
