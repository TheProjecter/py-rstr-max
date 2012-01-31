#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rstr_max import *
import re
import math
import sys
from optparse import OptionParser

import tool_stat as ts
import tool_math as tm

proxy_info = {'http': 'http://proxy.unicaen.fr:3128'}

def opt_parser_xp():
  parser = OptionParser()
  parser.add_option("-o", "--output_file", dest="fileout", default = "out.js",
                     help="Write report to FILEOUT (default)", metavar="FILEOUT")

  parser.add_option("-a", "--alphabet_size", dest="alphabet_size", default = 100, type="int",
                     help="set the number of different character to ALPHA", metavar="ALPHA")
  parser.add_option("-b", "--alphabet_step", dest="alphabet_step", default=10, type="int",
                     help="", metavar="ALPHA_STEP")

  parser.add_option("-p", "--nb_part", dest="nb_part", default = 1, type="int",
                     help="split the text in NB_PART", metavar="NB_PART")

  parser.add_option("-r", "--nb_run", dest="nb_run", default=20, type="int",
                     help="exec NB_RUN run", metavar="NB_RUN")
  parser.add_option("-i", "--limit_run", dest="limit_run", default=0, type="int",
                     help="erase the LIMIT_RUN first and last runs for the computation of the mean", metavar="LIMIT_RUN")

  parser.add_option("-l", "--len_max", dest="len_max", default=10*1000, type="int",
                     help="exploite a LEN_MAX string of random characters", metavar="LEN_MAX")
  parser.add_option("-s", "--len_step", dest="len_step", default=10, type="int",
                     help="", metavar="LEN_STEP")
  return parser

p = opt_parser_xp()
(o, _) = p.parse_args(sys.argv[1:])

signature = str(o)

step_run = o.len_max / o.len_step
step_alphabet = o.alphabet_size / o.alphabet_step

dic_occurs = {'global_signature' : signature, 'global_x' : 'alphabet size', 'global_y' : 'nb. occurences'}
dic_motifs = {'global_signature' : signature, 'global_x' : 'alphabet size', 'global_y' : 'nb. motifs'}
dic_avg = {'global_signature' : signature, 'global_x' : 'alphabet size', 'global_y' : 'avg. occurences per motifs'}
#dic_sd_motifs = {'global_legend' : 'standart deviation :: nb. occurences', 'global_x' : 'alphabet size', 'global_y' : 'nb. occurences'}
#dic_sd_occurs = {'global_legend' : 'standart deviation :: nb. occurences', 'global_x' : 'alphabet size', 'global_y' : 'nb. motifs'}

lc = ['r-','y-','b-','g-','r.','y.','b.','g.','r--','y--','b--','g--']

cpt = 0

for i in xrange(step_run, o.len_max+1, step_run) :
  list_x = []
  list_y_motifs = []
  list_y_occurs = []
  list_y_avg = []
#  list_y_sd_motifs = []
#  list_y_sd_occurs = []
  for alpha_size in xrange(step_alphabet, o.alphabet_size+1, step_alphabet) :
    motif, occ, avg, sd_motifs, sd_occurs = ts.run(i, alpha_size, o.nb_part, o.nb_run, o.limit_run)
    print '%s, %s, %s(%s), %s(%s), %s'%(alpha_size,i,motif,sd_motifs,occ,sd_occurs, avg)
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
