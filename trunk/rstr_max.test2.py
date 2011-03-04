#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools_karkkainen_sanders import *
from suffix_array import *
from rstr_max import *
import sys
import profile
import pstats

limit_recur = sys.getrecursionlimit()
sys.setrecursionlimit(limit_recur*limit_recur)

s = 'a' * 10

stat_str = 'stat'

for i in xrange(5) :
  s *= 2
  rstr = Rstr_max()
  str1_unicode = unicode(s,'utf-8','replace')
  rstr.add_str(str1_unicode)
  statname = '%s%s'%(stat_str,str(i))
  profile.run('rstr.go()',statname)
#  array_repeated = rstr.go()

for i in xrange(5) :
  statname = '%s%s'%(stat_str,str(i))  
  p = pstats.Stats(statname)
  p.print_stats()
