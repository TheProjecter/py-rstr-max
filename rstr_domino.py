#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from tools_karkkainen_sanders import *
#from suffix_array import *
#from rstr_max_verbose import *
from rstr_max import *
from string import *
import sys
from pprint import pprint

import re


def combinations(iterable, r) :
  # combinations('ABCD', 2) --> AB AC AD BC BD CD
  # combinations(range(4), 3) --> 012 013 023 123
  pool = tuple(iterable)
  n = len(pool)
  if r > n :
    return
  indices = range(r)
  yield tuple(pool[i] for i in indices)
  while True:
    for i in reversed(range(r)) :
      if indices[i] != i + n - r:
        break
    else :
      return
    indices[i] += 1
    for j in xrange(i+1, r) :
      indices[j] = indices[j-1] + 1
    yield tuple(pool[i] for i in indices)

def is_overlap(c1,c2) :
  '''c = (offset,longueur)'''
  assert (c1.start <= c2.start)
  return c1.start <= c2.start <= c1.start+c1.size

def is_in(d1,d2) :
  b1 = d2.get_start() <= d1.get_start() and d1.get_end() <= d2.get_end()
  if not b1 :
    return False
  b2 = d1.left.size <= d2.left.size and d1.right.size <= d2.right.size
  return b2

def print_domino(s, c1, c2) :
  '''c = offset, indice_alias
     alias[indice_alias] = graphie, longueur'''
  graphie1 = c1.graphie(s)
  graphie2 = c2.graphie(s)
  joker_len = c2.start -(c1.start+c1.size)
  s = graphie1 + '-'*joker_len + graphie2
  return '%-8s %s %s'%(s, c1, c2)

class DominoItem:
  def __init__(self, start, size, id_):
    self.start = start
    self.size = size
    self.id_ = id_ 
 
  def __str__(self):
    return '(%d,%d)'%(self.start, self.size)
  
  def __repr__(self):
    return '(%d,%d)'%(self.start, self.size)
 
  def graphie(self, s):
    return s[self.start:self.start+self.size]

  def getLenNonJoker(self) :
    return self.size

class Domino:
  def __init__(self, left, right):
    self.left = left
    self.right = right
    self.joker_len = right.start - (left.start+left.size)
    self.nonJoker_len = left.getLenNonJoker() + self.right.size

  def graphie(self,s,joker='-') :
    graphie1 = self.left.graphie(s)
    graphie2 = self.right.graphie(s)
    ss = graphie1 + joker*self.joker_len + graphie2
    return ss

  def get_start(self) :
    return self.left.start

  def get_end(self) :
    return self.right.start + self.right.size

  def __repr__(self) :
    return '(%d,%d)'%(self.get_start(), self.get_end())

  def get_len(self) :
    return self.right.size + self.right.start - self.left.start
  
  def getLenNonJoker(self) :
    return self.nonJoker_len

#str1 = 'tototiti'
#str1 = 'aaabaaa'
import sys
nb_a = int(sys.argv[1])
str1 = 'a'*nb_a + 'b' + 'a'*nb_a
#path = 'UNIX_user_data/sanitized_all.981115184025'
#str1 = file(path,'r').read()
#str1 = str1.replace('\n','#')
str1_unicode = unicode(str1,'utf-8','replace')

QUORUM = 2 #len(str1_unicode) / 10
print QUORUM
#print str1

rstr = Rstr_max()
rstr.add_str(str1_unicode)
r = rstr.go()

list_occurences = []

cpt = 0
for (offset_end, nb), (l, start_plage) in r.iteritems():
  ss = rstr.global_suffix[offset_end-l:offset_end]
#  print cpt, ss
  if nb < QUORUM :
    continue
  print repr(ss)
  print '  %s'%nb
  for o in xrange(start_plage, start_plage + nb) :
    offset_global = rstr.res[o]
    offset = rstr.idxPos[offset_global]
    list_occurences.append(DominoItem(offset,l,cpt))
  cpt += 1

print cpt

ld = []
#list_domino = []
result = {}

list_items = list_occurences

#for c1,c2 in combinations(list_occurences, 2) :
for c1 in list_occurences:
  for c2 in list_items:
    if c1.start > c2.start :
      continue
      #c1,c2 = c2,c1
 
    if not is_overlap(c1, c2) : 
      ld.append((c1,c2))
      key = (c1.id_, c2.start-(c1.start+c1.size), c2.id_)
      result.setdefault(key, []).append(Domino(c1, c2))
      #str_domino = print_domino(str1, c1,c2)
      #print str_domino
      #list_domino.append(str_domino)

for k, v in result.items():
  if len(v) < QUORUM:
    del result[k]

def cmp_domino(d1,d2) :
  return d1.get_start() - d2.get_start()

for k in result :
  result[k].sort(cmp_domino)

tauL = {}
for k, v in result.iteritems() :
  shift = v[0].left.start
  tauL[k] = tuple([d.left.start-shift for d in v])
#  print "%-8s %s"%(v[0].graphie(str1), tauL[k])

print "*"*20

import pprint
#for k, v in result.items():
#  print print_domino(str1, v[0].left, v[0].right), '**', k, v

res_ff = {}
for k, v in result.items():
  tau = tauL[k]
  if tau not in res_ff :
    res_ff[tau] = (k,v)
  else :
    ll = res_ff[tau][1][0].getLenNonJoker()
    cl = v[0].getLenNonJoker()
    if cl > ll:
      res_ff[tau] = (k,v)
    
for tau, (k, v) in res_ff.iteritems() :
  print "%-8s"%(repr(v[0].graphie(str1)))

print len(res_ff)
print 2**(nb_a-1) - 1
print (nb_a * 2 + 1)**(2*nb_a -1)



1/0


l = len(v)
for kk,vv in result.iteritems() :
  if kk == k :
    continue
  ll = len(vv)
  if l == ll :
#      print "'"*20
#      print print_domino(str1, v[0].left, v[0].right), '**', k, v
#      print print_domino(str1, vv[0].left, vv[0].right), '**', k, v
      
#      print is_in(v[0],vv[0])
    if is_in(v[0],vv[0]) :
      break
else :
  res_ff[k] = v



print "="*20
for k, v in res_ff.items():
  print print_domino(str1, v[0].left, v[0].right), '**', k, v


#pprint.pprint(res_ff)




#  print v[0].graphie(str1)
#for k, v in res_ff.items():
#  print print_domino(str1, v[0][0],v[0][1]), len(v)


#  rstr_domino.add_str(str_domino)
#print list_domino    
#print ld
#1/0


#print ld

1/0


res = {}
for (c1,c2) in ld :
  str_domino = print_domino(c1,c2,alias)
  if not res.has_key(str_domino) : res[str_domino] = []
  res[str_domino].append((c1,c2))

cpt = 0
for str_domino,list_domino in res.iteritems() :
  left_context = []
  right_context = []
  if len(list_domino) == 1 :
    continue
  print str_domino
  cpt += 1
  for (c1,c2) in list_domino :
    offset_car_left = c1[0] - 1
    offset_car_right = c2[0] + alias[c2[1]][1]
    if offset_car_left == -1 :
      car_left = 'START_STR'
    else :
      car_left = str1[offset_car_left]
    left_context.append(car_left)
    if offset_car_right == len(str1) :
      car_left = 'END_STR'
    else :
      car_left = str1[offset_car_right]
    right_context.append(car_left)
  print '  ',len(list_domino),left_context,right_context

print
print cpt


print res
1/0


di = {}
for d in list_domino :
  if not di.has_key(d) : di[d] = 0
  di[d] += 1

pprint(di)

#pprint(list_domino)

r_domino = rstr_domino.go()
res = []
ares = []
for ((id_str, end), nb), (l, start_plage) in r_domino.iteritems():
  ss = rstr_domino.array_str[id_str][end-l:end]
  cpt = 0
  atmp = []
  for i in xrange(start_plage, start_plage+nb) :
    su = rstr_domino.array_suffix[i]
    supstring = rstr_domino.array_str[su[1]]
    len_sup = len(supstring)
    if len_sup == l :
      cpt += 1
      atmp.append(su[1])
    if cpt == 2 :
      break
  if cpt >= 2 :
    ares.append(atmp)
    res.append(ss)

pprint(res)
pprint(ares)
for cpt,sl in enumerate(ares) :
  print res[cpt]
  print sl
  for i in sl :
    print ld[i]

#for d in list_domino :
#  print d 

