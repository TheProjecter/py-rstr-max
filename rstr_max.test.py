#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools_karkkainen_sanders import *
from suffix_array import *
from rstr_max import *
from string import *
import sys

limit_recur = sys.getrecursionlimit()
sys.setrecursionlimit(600000)

#str1 = open('ooo.txt','r').read()
str1 = "Otto von Bolschwing est mort sous le soleil de Sacramento (Californie), le 9 mars 1982. Il avait 72 ans et plusieurs vies derrière lui. Dans la première, ce rejeton de la noblesse allemande, membre des services de renseignement de la SS - l'ossature nazie du IIIe Reich - a exercé ses talents d'agent secret en Palestine. Devenu aide de camp du responsable des Affaires juives, Adolf Eichmann, il s'est attelé avec zèle à l'élaboration du programme d'extermination des juifs d'Europe. Après la guerre, le capitaine von Bolschwing a rejoint les rangs de la CIA, sous le nom de code de Grossbahn. En récompense de ses loyaux services, ses nouveaux maîtres lui ont offert une deuxième vie aux Etats-Unis, où l'ancien SS s'est taillé une belle carrière dans l'industrie. Jusqu'à devenir, en 1969, président de l'entreprise californienne de high-tech TCI."

str2 = "Otto va aux putes."

str1 = open('Sarkozy.htm','r').read()

str1_unicode = unicode(str1,'utf-8','replace')[:1000]
str2_unicode = unicode(str2,'utf-8','replace')

rstr = Rstr_max()
rstr.add_str(str1_unicode)
#rstr.add_str(str2_unicode)

import time
t = time.time()
array_repeated = rstr.go()
print time.time() - t
print len(array_repeated)

1/0

print "str length nb_occur"
for r in array_repeated :
  first_suffix = rstr.get_suffix(r[1][0])
  global_str = rstr.get_str(first_suffix[2])
  l = first_suffix[0] + r[0]
  s = global_str[first_suffix[0]:l].encode('utf-8', 'replace')
  set_str_occur = set()
  for id_suffix in r[1] :
    suffix = rstr.get_suffix(id_suffix)
    set_str_occur.add(suffix[2])
#  print "    ", set_str_occur
  if(len(set_str_occur) == 2) :
    print "[%s] %d %d"%(s, r[0], len(r[1])) 

#  for id_su in r[1] :

#    suffix = rstr.get_suffix(id_su)
#    str_corres = rstr.get_str(suffix[2])
#    foreach($rstr[1] as $id_su){
#      $suffix = $factory_rstr->__get_suffix($id_su);
#      $str_correspondante  = $factory_rstr->__get_str($suffix[2]);
#      echo "  string $suffix[2] - offset $suffix[0] - lenght $rstr[0]\n";
#    }
