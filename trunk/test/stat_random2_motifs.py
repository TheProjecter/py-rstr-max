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
                     help="erase the LIMIT_RUM first and last runs for the computation of the mean", metavar="LIMIT_RUN")

  parser.add_option("-l", "--len_max", dest="len_max", default=10*1000, type="int",
                     help="exploite a LEN_MAX string of random characters", metavar="LEN_MAX")
  parser.add_option("-s", "--len_step", dest="len_step", default=10, type="int",
                     help="", metavar="LEN_STEP")
  return parser

def run(len_str, len_alpha, nb_part, nb_run, extremum) :
  nb_different_motifs = []
  nb_occurs = []
  nb_occurs_avg = []
  stat_alpha = []
  for _ in xrange(nb_run) :
    rstr = Rstr_max()
#    rs = ts.random_string_athmospheric(len_str,len_alpha,proxy_info)
    rs = ts.random_string(len_str,len_alpha)
    lp = ts.cut_str(rs,nb_part)
#    rl = 0
    for substring in lp :
#      rl += len(substring)
      rstr.add_str(substring)
    r = rstr.go()

    nb_different_motifs_run = len(r.keys())
    nb_different_motifs.append(nb_different_motifs_run)
    sum_nb_occ = sum([nb for (_, nb) in r.keys()])
    nb_occurs_avg.append(sum_nb_occ / nb)
    nb_occurs.append(sum_nb_occ)

  if extremum > 0 :
    nb_different_motifs.sort()
    nb_different_motifs = nb_different_motifs[extremum:-extremum]
    nb_occurs.sort()
    nb_occurs = nb_occurs[extremum:-extremum]
    nb_occurs_avg.sort()
    nb_occurs_avg = nb_occurs[extremum:-extremum]

  sd_motifs = tm.standart_deviation(nb_different_motifs)  
  sd_occurs = tm.standart_deviation(nb_occurs)  

  moy = sum(nb_different_motifs) / len(nb_different_motifs)
  moy_occur = sum(nb_occurs) / len(nb_occurs)
  avg_occur = sum(nb_occurs_avg) / len(nb_occurs_avg)
  return moy, moy_occur, avg_occur, sd_motifs, sd_occurs

p = opt_parser_xp()
(o, _) = p.parse_args(sys.argv[1:])

step_run = o.len_max / o.len_step
step_alphabet = o.alphabet_size / o.alphabet_step

dic_occurs = {'global_legend' : 'nb. occurences', 'global_x' : 'len str', 'global_y' : 'nb. occurences'}
dic_motifs = {'global_legend' : 'nb. motifs', 'global_x' : 'len_str', 'global_y' : 'nb. motifs'}
dic_avg = {'global_legend' : 'nb. motifs', 'global_x' : 'len_str', 'global_y' : 'avg. occurences per motif'}
dic_sd_motifs = {'global_legend' : 'standart deviation :: nb. occurences', 'global_x' : 'len_str', 'global_y' : 'nb. occurences'}
dic_sd_occurs = {'global_legend' : 'standart deviation :: nb. motifs', 'global_x' : 'len_str', 'global_y' : 'nb. motifs'}

lc = ['r-','ro','yo','bo','go','r^','y^','b^','g^','r--']

cpt = 0

for alpha_size in xrange(step_alphabet, o.alphabet_size+1, step_alphabet) :
  list_x = []
  list_y_motifs = []
  list_y_occurs = []
  list_y_avg = []
  list_y_sd_motifs = []
  list_y_sd_occurs = []
  for i in xrange(step_run, o.len_max+1, step_run) :
    r, occ, avg, sd_motifs, sd_occurs = ts.run(i, alpha_size, o.nb_part, o.nb_run, o.limit_run)
    print '%s, %s, %s(%s), %s(%s), %s'%(alpha_size, i, r, sd_motifs, occ, sd_occurs, avg)
    list_x.append(i)
    list_y_motifs.append(r)
    list_y_occurs.append(occ)
    list_y_avg.append(avg)
    list_y_sd_motifs.append(sd_motifs)
    list_y_sd_occurs.append(sd_occurs)

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

  dic_sd_occurs[alpha_size] = {'style_plot':'%s'%lc[cpt],
                               'name_legend':'(alpha:%s)'%(alpha_size),
                               'list_x':list_x,
                               'list_y':list_y_sd_occurs}
  dic_sd_motifs[alpha_size] = {'style_plot':'%s'%lc[cpt],
                               'name_legend':'(alpha:%s)'%(alpha_size),
                               'list_x':list_x,
                               'list_y':list_y_sd_motifs}
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
file_out = open('%s_%s'%('sd_occ',o.fileout),'w')
file_out.write(str(dic_sd_occurs))
file_out.close()
file_out = open('%s_%s'%('sd_mot',o.fileout),'w')
file_out.write(str(dic_sd_motifs))
file_out.close()
