#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from tools_karkkainen_sanders import *
#from suffix_array import *
#from rstr_max_verbose import *
from rstr_max import *
from string import *
import sys
from pprint import pprint

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
  assert (c1[0] <= c2[0])
  return c1[0] <= c2[0] <= c1[0]+c1[1]

def print_domino(c1, c2, alias) :
  '''c = offset, indice_alias
     alias[indice_alias] = graphie, longueur'''
  graphie1 = alias[c1[1]][0]
  graphie2 = alias[c2[1]][0]
  joker_len = abs(c1[0] + alias[c1[1]][1] - c2[0])
  joker_write = '-'*joker_len
  return '%s%s%s'%(graphie1,joker_write,graphie2)

#str1 = 'tototiti'
#str1 = 'aaabaaa'
str1 = 'a'*20 + 'b' + 'a'*20
str1_unicode = unicode(str1,'utf-8','replace')

rstr = Rstr_max()
rstr.add_str(str1_unicode)
r = rstr.go()

list_occurences = []
alias = [0] * len(r.keys())
cpt = 0

list_combinations = []

def do_combination(l, occurence):
  pass

for ((id_str, end), nb), (l, start_plage) in r.iteritems():
  ss = rstr.array_str[id_str][end-l:end]
  for i in xrange(start_plage, start_plage+nb) :
    list_occurences.append((rstr.array_suffix[i][0], cpt))
  alias[cpt] = (ss,l)
  cpt += 1

ld = []
list_domino = []
rstr_domino = Rstr_max()

for c1,c2 in combinations(list_occurences, 2) :
  if c1[0] > c2[0] :
    c1,c2 = c2,c1
  o1,a1 = c1
  o2,a2 = c2

  s1,l1 = alias[a1]
  s2,l2 = alias[a2]
  if not is_overlap((o1,l1), (o2,l2)) : 
    ld.append((c1,c2))
    str_domino = print_domino(c1,c2,alias)
    list_domino.append(str_domino)
    rstr_domino.add_str(str_domino)
#print list_domino    
#print ld
#1/0

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

1/0


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

