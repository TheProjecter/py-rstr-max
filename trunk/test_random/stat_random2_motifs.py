#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rstr_max import *
import re
import math
import sys

import tool_stat as ts
import tool_math as tm

proxy_info = {'http': 'http://proxy.unicaen.fr:3128'}

p = ts.opt_parser_xp()
(o, _) = p.parse_args(sys.argv[1:])

signature = str(o)

step_run = o.len_max / o.len_step
step_alphabet = o.alphabet_size / o.alphabet_step

dic_occurs = {'global_signature' : signature, 'global_x' : 'len str', 'global_y' : 'nb. occurences'}
dic_motifs = {'global_signature' : signature, 'global_x' : 'len_str', 'global_y' : 'nb. motifs'}
dic_avg = {'global_signature' : signature, 'global_x' : 'len_str', 'global_y' : 'avg. occurences per motif'}
#dic_sd_motifs = {'global_x' : 'len_str', 'global_y' : 'std deviation :: nb. occurences'}
#dic_sd_occurs = {'global_x' : 'len_str', 'global_y' : 'std_deviation :: nb. motifs'}

lc = ['r-','y-','b-','g-','r.','y.','b.','g.','r--','y--','b--','g--']

cpt = 0

for alpha_size in xrange(step_alphabet, o.alphabet_size+1, step_alphabet) :
  list_x = []
  list_y_motifs = []
  list_y_occurs = []
  list_y_avg = []
#  list_y_sd_motifs = []
#  list_y_sd_occurs = []
  for i in xrange(step_run, o.len_max+1, step_run) :
    motif, occ, avg, sd_motifs, sd_occurs = ts.run(i, alpha_size, o.nb_part, o.nb_run, o.limit_run)
    print '%s, %s, %s(%s), %s(%s), %s'%(alpha_size, i, motif, sd_motifs, occ, sd_occurs, avg)
    list_x.append(i)
    list_y_motifs.append(motif)
    list_y_occurs.append(occ)
    list_y_avg.append(avg)
#    list_y_sd_motifs.append(sd_motifs)
#    list_y_sd_occurs.append(sd_occurs)

  dic_occurs[alpha_size] = {'style_plot':'%s'%lc[cpt],
                            'name_legend':'(alpha:%s)'%(alpha_size),
                            'list_x':list_x,
                            'list_y':list_y_occurs}
  dic_motifs[alpha_size] = {'style_plot':'%s'%lc[cpt],
                            'name_legend':'(alpha:%s)'%(alpha_size),
                            'list_x':list_x,
                            'list_y':list_y_motifs}
  dic_avg[alpha_size] = {'style_plot':'%s'%lc[cpt],
                         'name_legend':'(alpha:%s)'%(alpha_size),
                         'list_x':list_x,
                         'list_y':list_y_avg}

#  dic_sd_occurs[alpha_size] = {'style_plot':'%s'%lc[cpt],
#                               'name_legend':'(alpha:%s)'%(alpha_size),
#                               'list_x':list_x,
#                               'list_y':list_y_sd_occurs}
#  dic_sd_motifs[alpha_size] = {'style_plot':'%s'%lc[cpt],
#                               'name_legend':'(alpha:%s)'%(alpha_size),
#                               'list_x':list_x,
#                               'list_y':list_y_sd_motifs}
  cpt += 1

file_out = open('%s_%s'%('occ',o.fileout),'w')
file_out.write(str(dic_occurs))
file_out.close()
file_out = open('%s_%s'%('mot',o.fileout),'w')
file_out.write(str(dic_motifs))
file_out.close()
file_out = open('%s_%s'%('avg',o.fileout),'w')
file_out.write(str(dic_avg))
file_out.close()
#file_out = open('%s_%s'%('sd_occ',o.fileout),'w')
#file_out.write(str(dic_sd_occurs))
#file_out.close()
#file_out = open('%s_%s'%('sd_mot',o.fileout),'w')
#file_out.write(str(dic_sd_motifs))
#file_out.close()
