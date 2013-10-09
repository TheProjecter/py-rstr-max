#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rstr_max import *
import sys

#str1 = 'tititoto'
#str1 = 'a'*10

#f = file('test.xml','r')
#s = f.read()
#f.close()

s = "ABCDABCABD"
s = 'tititoto'
str1_unicode = unicode(s,'utf-8','replace')

def test(list_str) :
  rstr = Rstr_max()
  for i,r in enumerate(list_str) :
    rstr.add_str(r)
  res = rstr.go()
  l_indice = []
  l_rstr = []
  for (offset_end, nb), (l, start_plage) in res.iteritems():
    ss = rstr.global_suffix[offset_end-l:offset_end]
    id_chaine = rstr.idxString[offset_end-1]
    s = rstr.array_str[id_chaine]
    print s[offset_end-l:offset_end]
    l_indice.append((offset_end,nb))
    l_rstr.append(ss)
  return l_indice,l_rstr,res,rstr

cpt = 0
limit = 40
lr = [str1_unicode]

history = []

print test(lr)
exit(0)

while len(lr) > 0:
  li,lr,res,r = test(lr)
  history.append((li,lr,res,r))
  cpt += 1

for li,lr,res,rstr in history :
  print "*"*40
  print li
  print lr



