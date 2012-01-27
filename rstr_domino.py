#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from tools_karkkainen_sanders import *
#from suffix_array import *
#from rstr_max_verbose import *
from rstr_max import *
from string import *
import sys
import re

def maximal_equiv_motif(motif, s, index) :
  len_left = motif.first_char() 
  len_right = len(s) - motif.last_char()
  length = len_left + motif.length + len_right
  content = []
  gap = []

  flag = False
  start = -1
  list_space = []
  for i in xrange(-len_left, length-len_left) :
    char = s[i+len_left]
    for l in motif.L :
      if s[l + i] != char :
        if flag :
          end = i + len_left
          k = (start, end-start)
          content.append(k)
          start = end
          flag = False
        break
    else :
      if not flag :
        end = i + len_left
        if start != -1 :
          list_space.append(end-start)
        start = end
        flag = True
  if flag :
     end = i + len_left + 1 
     k = (start, end-start)
     content.append(k)

  new_L = [content[0][0]+offset-len_left for offset in motif.L]
  list_id_motif = [index[k] for k in content]

  return (tuple(list_id_motif),tuple(list_space)), new_L

def mix_motif_bak(dic_gapped_motifs, list_motifs, s, index_motifs, quorum) :
  dic_res = {}
  for idx_gapped, gapped_motif in dic_gapped_motifs.iteritems() :
    for motif in list_motifs :
      new_dic_gapped_motifs = add_motif(gapped_motif, motif, s, list_motifs, index_motifs, quorum)
      for new_idx, new_gapped_motif in new_dic_gapped_motifs.iteritems():
        dic_res[new_idx] = new_gapped_motif
  return dic_res

def add_motif(gapped_motif, motif, s, list_motifs, index_motifs, quorum) :
  id_content = list(gapped_motif.list_idMotif)
  id_space = list(gapped_motif.list_space)

  id_motif = motif.idx

  res = {}
  for start_gapped in gapped_motif.L :
    end_gapped = start_gapped + gapped_motif.length -1
    for start_motif in motif.L :
      if end_gapped >= start_motif:
        continue
      new_id_content = id_content + [id_motif]
      new_id_space = id_space + [start_motif - end_gapped]
      new_id = (tuple(new_id_content),tuple(new_id_space))
#      m = GappedMotif((new_id_content,new_id_space), L, list_motifs)
      res.setdefault(new_id, []).append(start_gapped) 

  new_gapped_motifs = {}
  for key, L in res.iteritems() :
    if len(L) >= quorum :
      m = GappedMotif(key, L, list_motifs)
      new_key, L = maximal_equiv_motif(m, s, index_motifs)
      new_gapped_motifs[new_key] = GappedMotif(new_key, L, list_motifs)

  return new_gapped_motifs

def mix_motif(dic_gapped_motifs, list_motifs, s, index_motifs, quorum) :
  dic_res = {}
  for (id_content,id_space), gapped_motif in dic_gapped_motifs.iteritems() :
    id_content = list(id_content)
    id_space = list(id_space)
    for motif in list_motifs :

      res = add_motif(gapped_motif, motif, s, list_motifs, index_motifs, quorum)
      for new_key, new_gapped_motif in res.iteritems() :
        dic_res[new_key] = new_gapped_motif
      continue

      id_motif = motif.idx
      res = {}
      for start_gapped in gapped_motif.L :
        end_gapped = start_gapped + gapped_motif.length -1
        for start_motif in motif.L :
          if end_gapped >= start_motif :
            continue
          new_id_content = id_content + [id_motif]
          new_id_space = id_space + [start_motif - end_gapped]
          new_id = (tuple(new_id_content),tuple(new_id_space))
          res.setdefault(new_id, []).append(start_gapped) 

      for key, L in res.iteritems() :
        if len(L) >= quorum :
          m = GappedMotif(key, L, list_motifs)
          new_key, L = maximal_equiv_motif(m, s, index_motifs)
          dic_res[new_key] = GappedMotif(new_key, L, list_motifs)

  return dic_res


class Motif() :
  def __init__(self, idx, length, L) :
    self.idx = idx
    self.length = length
    self.L = L
#    self.L.sort()

  def graphie(self, s) :
    return s[self.L[0]:self.L[0]+self.length]

  def first_char(self) :
    return self.L[0]
#    return min(self.L)

  def last_char(self) :
    return self.L[-1] + self.length
#    return max(self.L) + self.length

class GappedMotif() :
  def __init__(self, idx, L, list_motif) :
    self.list_idMotif = idx[0]
    self.list_space = idx[1]
    self.L = L
#    self.L.sort()
    self.length = self.get_len(list_motif)

  def get_len(self,list_motif) :
    length = sum(self.list_space)
    for id_motif in self.list_idMotif :
      length += list_motif[id_motif].length
    return length

  def graphie(self,s,list_motif) :
    res = ''
    for i,len_space in enumerate(self.list_space) :
      id_motif = self.list_idMotif[i]
      res += list_motif[id_motif].graphie(s)
      res += '-'*len_space
    id_motif = self.list_idMotif[-1]
    res += list_motif[id_motif].graphie(s)
    return res

  def first_char(self) :
    return self.L[0]
#    return min(self.L)

  def last_char(self) :
    return self.L[-1] + self.length
#    return max(self.L) + self.length

#nb_a = int(sys.argv[1])
#str1 = 'a'*nb_a + 'b' + 'a'*nb_a
#str1 = 'HATTIVAHATTIVHTTTIVAT'
#str1 = 'HATTIVATTIAA'
#str1 = 'tititoto'
#path = 'UNIX_user_data/sanitized_all.981115184025'
path = './002.art'
str1 = file(path,'r').read()
#str1 = str1.replace('\n','#')
s = unicode(str1,'utf-8','replace')
s = s[0:1000]
pat_tag = re.compile('</*[^>]+/*>', re.I | re.M)
s = pat_tag.sub('', s)
pat_space = re.compile('[\s]+', re.I | re.M)
s = pat_space.sub(' ', s)

QUORUM = 2
#QUORUM = len(s) / 10

rstr = Rstr_max()
rstr.add_str(s)
r = rstr.go()

list_motifs = []

cpt = 0

index_motifs = {}

for (offset_end, nb), (size, start_plage) in r.iteritems():
  ss = rstr.global_suffix[offset_end-size:offset_end]
  if nb < QUORUM :
    continue
  L = []
  for o in xrange(start_plage, start_plage + nb) :
    offset_global = rstr.res[o]
    offset = rstr.idxPos[offset_global]
    L.append(offset)
    index_motifs[(offset,size)] = cpt
  L.sort()
  motif = Motif(cpt,size,L)
  list_motifs.append(motif)
  cpt += 1

print len(list_motifs)

flag = False
dic_gapped_motifs = {}
tmp = {}
tmp_l = {}

for motif in list_motifs :
  (content,space),L = maximal_equiv_motif(motif, s, index_motifs)
  m = GappedMotif((content,space), L, list_motifs)
#  if (content,space) in dic_gapped_motifs :
#    print tmp[(content,space)].graphie(s)
#    print tmp_l[(content,space)]
#    flag = True
  dic_gapped_motifs[(content,space)] = m
  tmp.setdefault((content,space), []).append(motif)
  tmp_l.setdefault((content,space), []).append(L)

#  if flag :
#    print tmp[(content,space)].graphie(s)
#    print tmp_l[(content,space)]
#    print dic_gapped_motifs[(content,space)].graphie(s,list_motifs)
#    print "="*20
#  flag = False


#  (nc,ns),nL = maximal_equiv_motif(m, s, index_motifs)
#  assert(nc==content)
#  assert(ns==space)
#  assert(nL == L)
#1/0
for k,v in tmp.iteritems() :
  if len(v) == 1 :
    continue
  for m in v :
    print '[',m.graphie(s).encode('utf-8'),']'
    print m.L
  for l in tmp_l[k] :
    print l
  print

print len(dic_gapped_motifs)
1/0

all_motifs = {}
for k,m in dic_gapped_motifs.iteritems() :
  all_motifs[k] = m

cpt = 0
while dic_gapped_motifs :
  dic_gapped_motifs = mix_motif(dic_gapped_motifs, list_motifs, s, index_motifs, QUORUM)
  print cpt, len(dic_gapped_motifs)
  for k,m in dic_gapped_motifs.iteritems() :
    if len(k[0]) > 1 :
      all_motifs[k] = m
  cpt += 1

cpt = 0
for k,m in all_motifs.iteritems() :
  if len(k[0]) != 1 :
    cpt += 1
#  print k, m.graphie(s, list_motifs)

print
print len(all_motifs)
print cpt
