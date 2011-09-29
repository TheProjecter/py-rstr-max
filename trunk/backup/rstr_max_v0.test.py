#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools_karkkainen_sanders import *
#from suffix_array import *
from rstr_max_v0 import *
import sys

limit_recur = sys.getrecursionlimit()
sys.setrecursionlimit(600000)

str1 = "Otto von Bolschwing est mort sous le soleil de Sacramento (Californie), le 9 mars 1982. Il avait 72 ans et plusieurs vies derrière lui. Dans la première, ce rejeton de la noblesse allemande, membre des services de renseignement de la SS - l'ossature nazie du IIIe Reich - a exercé ses talents d'agent secret en Palestine. Devenu aide de camp du responsable des Affaires juives, Adolf Eichmann, il s'est attelé avec zèle à l'élaboration du programme d'extermination des juifs d'Europe. Après la guerre, le capitaine von Bolschwing a rejoint les rangs de la CIA, sous le nom de code de Grossbahn. En récompense de ses loyaux services, ses nouveaux maîtres lui ont offert une deuxième vie aux Etats-Unis, où l'ancien SS s'est taillé une belle carrière dans l'industrie. Jusqu'à devenir, en 1969, président de l'entreprise californienne de high-tech TCI."

str1_unicode = unicode(str1,'utf-8','replace')
str2_unicode = str1_unicode[::-1]

rstr = Rstr_max()
rstr.add_str(str1_unicode)
rstr.add_str(str2_unicode)
array_repeated = rstr.go()

for r in array_repeated :
  first_suffix = rstr.get_suffix(r[1][0])
  global_str = rstr.get_str(first_suffix[2])
  l = r[0]
  s = global_str[first_suffix[0]:first_suffix[0]+l].encode('utf-8')
  print s, r[0]
  for id_suffix in r[1] :
    su = rstr.array_suffix[id_suffix]
    ss = rstr.array_str[su[2]][su[0]:su[0]+l].encode('utf-8')
    print '    ',ss, su[0], su[0]+l, su[2]
    assert(s == ss)
#    print ss

#print "πάλιν / δρόμος"
#for r in array_repeated :
#  first_suffix = rstr.get_suffix(r[1][0])
#  global_str = rstr.get_str(first_suffix[2])
#  l = first_suffix[0] + r[0]
#  s = global_str[first_suffix[0]:l].encode('utf-8', 'replace')
#  set_str_occur = set()
##  print s, len(r[1])
#  for id_suffix in r[1] :
#    suffix = rstr.get_suffix(id_suffix)
#    set_str_occur.add(suffix[2])
#  if(len(set_str_occur) == 2) :
#    print "[%s] %d %d"%(s, r[0], len(r[1]))
