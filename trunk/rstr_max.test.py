#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rstr_max import *
from tools_karkkainen_sanders import *
import sys

rstr = Rstr_max()
#s1 = ['ab','abc','ab']
#rstr.add_str(s1)
#rstr.add_str(s1)

#r = rstr.go_word()
#s1 = 'tototiti'
#s1 = ['je']*10

#s1 = 'HATTIV1'
#s2 = 'ATTIAA0'

p = ord(' ')
a = unichr(p-1).encode('utf-8')
b = unichr(p-2).encode('utf-8')
c = unichr(p-3).encode('utf-8')

s1 = 'Tajlandzki rząd ostrzega kobiety przed noszeniem czarnych legginsów, gdyż ciemne kolory przyciągają komary, przenoszące dengę.%s'%b
s2 = 'W tym roku w Tajlandii odnotowano ponad 45 tys. przypadków dengi, czyli o 40%s więcej niż w ubiegłym roku.%s'%('%',c)
s = s1 + s2

rstr.add_str(s)
r = rstr.go()

res = []

def cmp_len(a,b) :
  return -(len(a) - len(b))

for (offset_end, nb), (l, start_plage) in r.iteritems():
  ss = rstr.global_suffix[offset_end-l:offset_end]
  id_chaine = rstr.idxString[offset_end-1]
#  s = rstr.array_str[id_chaine]
  repeat = rstr.get_repeat(id_chaine, rstr.idxPos[offset_end-l], l)
  res.append(repeat)

res.sort(cmp_len)
print res


#  print '[%s]'%(repeat)
#  print ss
#  print '[%s] %d'%(ss.encode('utf-8'), nb)

#  for o in range(start_plage, start_plage + nb) :
#    offset_global = rstr.res[o]
#    offset = rstr.idxPos[offset_global]
#    id_str = rstr.idxString[offset_global]
#    print '  ',rstr.get_repeat(id_str, offset, l), id_str, offset, l

#    print '   (%i, %i)'%(offset, id_str)

#    sss = rstr.global_suffix[offset_global:offset_global+l]
#    print '   ',sss

#    sss = rstr.array_str[id_str][offset:offset+l]
#    print '   ',sss
