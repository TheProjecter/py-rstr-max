#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rstr_max import *
import re
import math
import sys
import os

import tool_stat as ts
import tool_math as tm

proxy_info = {'http': 'http://proxy.unicaen.fr:3128'}

p = ts.opt_parser_xp_random()
(o, _) = p.parse_args(sys.argv[1:])

signature = str(o)

len_min = int(o.string_info[0])
len_max = int(o.string_info[1])
len_step = int(o.string_info[2])
#len_size = len_max - len_min

alphabet_min = int(o.alphabet_info[0])
alphabet_max = int(o.alphabet_info[1])
alphabet_step = int(o.alphabet_info[2])
#alphabet_size = alphabet_max - alphabet_min

step_run = len_step
step_alphabet = alphabet_step

#step_run = len_max / len_step
#step_alphabet = alphabet_size / alphabet_step

if os.path.isdir(o.dirout) == False :
  os.makedirs(o.dirout)
dir_xp_len = os.path.join(o.dirout,'len')
if os.path.isdir(dir_xp_len) == False :
  os.makedirs(dir_xp_len)

dic_occurs = {'global_signature' : signature, 'global_x' : 'alphabet size', 'global_y' : 'nb. occurences'}
dic_motifs = {'global_signature' : signature, 'global_x' : 'alphabet size', 'global_y' : 'nb. motifs'}
dic_avg = {'global_signature' : signature, 'global_x' : 'alphabet size', 'global_y' : 'avg. occurences per motifs'}


#dic_sd = {'global_signature' : signature, 'global_x' : 'alphabet size', 'global_y' : 'standart deviation :: occurences per motifs'}
#dic_sd_motifs = {'global_legend' : 'standart deviation :: nb. occurences', 'global_x' : 'alphabet size', 'global_y' : 'nb. occurences'}
#dic_sd_occurs = {'global_legend' : 'standart deviation :: nb. occurences', 'global_x' : 'alphabet size', 'global_y' : 'nb. motifs'}

lc = ['r-','y-','b-','g-','r.','y.','b.','g.','r--','y--','b--','g--']

cpt = 0

def treat_info_len(dic_len, prefix_js, dir_xp_len, str_size, alpha_size):
  list_len_x = sorted(dic_len.keys())
  list_len_y = [dic_len[x] for x in list_len_x]
  name_graph_len = '%s_len_%d_alpha_%06d.js'%(prefix_js, str_size, alpha_size)
  path_graph_len = os.path.join(dir_xp_len,name_graph_len)
  dic_out = {'global_signature' : signature,
             'global_x' : 'len_motif',
             'global_y' : 'nb. occurences motifs'}
  dic_out[0] = {'style_plot':'r-',
                'name_legend':'(len:%s,alpha:%s)'%(str_size,alpha_size),
                'list_x':list_len_x,
                'list_y':list_len_y}
  file_out = open('%s'%(path_graph_len),'w')
  file_out.write(str(dic_out))
  file_out.close()

for i in xrange(len_min, len_max+1, step_run) :
  list_x = []
  list_y_motifs = []
  list_y_occurs = []
  list_y_avg = []
#  list_y_sd = []
#  list_y_sd_motifs = []
#  list_y_sd_occurs = []
  for alpha_size in xrange(alphabet_min, alphabet_max+1, step_alphabet) :
#   motif, occ, avg, sd_motifs, sd_occurs, dic_occ_len, dic_mot_len = ts.run(i, alpha_size, o.nb_part, o.nb_run, o.limit_run)
    motif, occ, avg, dic_occ_len, dic_mot_len = ts.run(i, alpha_size, o.nb_part, o.nb_run, o.limit_run)
    treat_info_len(dic_occ_len, "occ", dir_xp_len, i, alpha_size)
    treat_info_len(dic_mot_len, "mot", dir_xp_len, i, alpha_size)

#    print '%s, %s, %s(%s), %s(%s), %s'%(alpha_size,i,motif,sd_motifs,occ,sd_occurs, avg)
    print '%s, %s, %s, %s, %s'%(alpha_size, i, motif, occ, avg)
    list_x.append(alpha_size)
    list_y_motifs.append(motif)
    list_y_occurs.append(occ)
    list_y_avg.append(avg)
#    list_y_sd_motifs.append(sd_motifs)
#    list_y_sd_occurs.append(sd_occurs)

  dic_occurs[i] = {'style_plot':'%s'%lc[cpt],
                   'name_legend':'(len:%s)'%(i),
                   'list_x':list_x,
                   'list_y':list_y_occurs}
  dic_motifs[i] = {'style_plot':'%s'%lc[cpt],
                   'name_legend':'(len:%s)'%(i),
                   'list_x':list_x,
                   'list_y':list_y_motifs}
  dic_avg[i] = {'style_plot':'%s'%lc[cpt],
                'name_legend':'(len:%s)'%(i),
                'list_x':list_x,
                'list_y':list_y_avg}

#  dic_sd_occurs[i] = {'style_plot':'%s'%lc[cpt],
#                      'name_legend':'(len:%s)'%(i),
#                      'list_x':list_x,
#                      'list_y':list_y_sd_occurs}
#  dic_sd_motifs[i] = {'style_plot':'%s'%lc[cpt],
#                      'name_legend':'(len:%s)'%(i),
#                      'list_x':list_x,
#                      'list_y':list_y_sd_motifs}
  cpt += 1

p_occ = os.path.join(o.dirout,'%s_%s'%('occ',o.fileout))
file_out = open('%s'%p_occ,'w')
file_out.write(str(dic_occurs))
file_out.close()
p_mot = os.path.join(o.dirout,'%s_%s'%('mot',o.fileout))
file_out = open('%s'%p_mot,'w')
file_out.write(str(dic_motifs))
file_out.close()
p_avg = os.path.join(o.dirout,'%s_%s'%('avg',o.fileout))
file_out = open('%s'%p_avg,'w')
file_out.write(str(dic_avg))
file_out.close()
#file_out = open('%s_%s'%('sd_occ',o.fileout),'w')
#file_out.write(str(dic_sd_occurs))
#file_out.close()
#file_out = open('%s_%s'%('sd_mot',o.fileout),'w')
#file_out.write(str(dic_sd_motifs))
#file_out.close()
