#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from tools_karkkainen_sanders import *
#from suffix_array import *
#from rstr_max_verbose import *
from rstr_max import *
from string import *
import sys

rstr = Rstr_max()
str1 = 'a'*1000000 #'tototiti'
#str1 = str1 + 'b' + str1
str1_unicode = unicode(str1,'utf-8','replace')
rstr.add_str(str1_unicode)
# str2 = 'b' #'a'*10 #'tototiti'
# str2_unicode = unicode(str2,'utf-8','replace')
# rstr.add_str(str2_unicode)
# str2 = 'b' #'a'*10 #'tototiti'
# str2_unicode = unicode(str2,'utf-8','replace')
# rstr.add_str(str2_unicode)
r = rstr.go()

print "res", len(r)

#import profile
#profile.run('rstr.go()')

#raise SystemExit(0)

#for (id_str, end, nb), (l, start_plage) in r.iteritems():
#  ss = rstr.array_str[id_str][end-l:end]
##  if len(ss) > 8 :
#  print '[%s] %d'%(ss.encode('utf-8'), nb)

#  for o in range(start_plage, start_plage + nb) :
#    su = rstr.array_suffix[o]
#    print '   ' + str(su)
#    sss = rstr.array_str[su[1]][su[0]:su[0]+l]
#    if ss != sss :
#      print ss, sss