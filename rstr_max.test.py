#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from tools_karkkainen_sanders import *
#from suffix_array import *
#from rstr_max_verbose import *
from rstr_max import *
from string import *
import sys

str1 = "Otto von Bolschwing est mort sous le soleil de Sacramento (Californie), le 9 mars 1982. Il avait 72 ans et plusieurs vies derrière lui. Dans la première, ce rejeton de la noblesse allemande, membre des services de renseignement de la SS - l'ossature nazie du IIIe Reich - a exercé ses talents d'agent secret en Palestine. Devenu aide de camp du responsable des Affaires juives, Adolf Eichmann, il s'est attelé avec zèle à l'élaboration du programme d'extermination des juifs d'Europe. Après la guerre, le capitaine von Bolschwing a rejoint les rangs de la CIA, sous le nom de code de Grossbahn. En récompense de ses loyaux services, ses nouveaux maîtres lui ont offert une deuxième vie aux Etats-Unis, où l'ancien SS s'est taillé une belle carrière dans l'industrie. Jusqu'à devenir, en 1969, président de l'entreprise californienne de high-tech TCI."

#str1 = 'abc'

str1_unicode = unicode(str1,'utf-8','replace')
str2_unicode = str1_unicode[::-1]

rstr = Rstr_max()
rstr.add_str(str1_unicode)
rstr.add_str(str2_unicode)
r = rstr.go()

for ((id_str, end), nb), (l, start_plage) in r.iteritems():
  ss = rstr.array_str[id_str][end-l:end]
  print ss
  for o in range(start_plage, start_plage + nb) :
    su = rstr.array_suffix[o]
#    print '   ' + str(su)
    sss = rstr.array_str[su[1]][su[0]:su[0]+l]
    if ss != sss :
      print ss, sss
