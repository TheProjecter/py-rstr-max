#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rstr_max import *
import tool_math as tm
import random
import array
import urllib
import os
from optparse import OptionParser

def read_list_arg1(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

def opt_parser_xp_random():
  parser = OptionParser()
  parser.add_option("-o", "--output_file", dest="fileout", default = "out.js",
                     help="Write report to FILEOUT [default : out.js]", metavar="FILEOUT")
  parser.add_option("-d", "--output_dir", dest="dirout", default = ".",
                     help="Write report to DIROUT [default : ./]", metavar="DIROUT")

#  parser.add_option("-a", "--alphabet_size", dest="alphabet_size", default = 100, type="int",
#                     help="set the number of different character to ALPHA", metavar="ALPHA")
#  parser.add_option("-b", "--alphabet_step", dest="alphabet_step", default=10, type="int",
#                     help="", metavar="ALPHA_STEP")

  parser.add_option(
    "-a", "--aphabet_info", dest= "alphabet_info", default = ["2","101","2"],
    type = "string", action = "callback", callback = read_list_arg1,
    help="APLHA min_apha,max_alpha,step_alpha [default : -a 2,101,2]",
    metavar="AlPHA")
  parser.add_option(
    "-s", "--string_info", dest= "string_info", default = ["10000","100001","10000"],
    type = "string", action = "callback", callback = read_list_arg1,
    help="STRING min_string,max_string,step_string [default : -a 10000,100001,10000]",
    metavar="STRING")

#  parser.add_option("-l", "--len_max", dest="len_max", default=10*1000, type="int",
#                     help="exploite a LEN_MAX string of random characters", metavar="LEN_MAX")
#  parser.add_option("-s", "--len_step", dest="len_step", default=10, type="int",
#                     help="", metavar="LEN_STEP")

  parser.add_option("-p", "--nb_part", dest="nb_part", default = 1, type="int",
                     help="split the text in NB_PART", metavar="NB_PART")
  parser.add_option("-r", "--nb_run", dest="nb_run", default=20, type="int",
                     help="exec NB_RUN run", metavar="NB_RUN")
  parser.add_option("-i", "--limit_run", dest="limit_run", default=0, type="int",
                     help="erase the LIMIT_RUN first and last runs for the computation of the mean", metavar="LIMIT_RUN")

  return parser

def opt_parser_xp_random_atomic():
  parser = OptionParser()

  parser.add_option("-o", "--output_file", dest="fileout", default = "out.js",
                     help="Write report to FILEOUT [default : out.js]", metavar="FILEOUT")

  parser.add_option("-d", "--output_dir", dest="dirout", default = ".",
                     help="Write report to DIROUT [default : ./]", metavar="DIROUT")

  parser.add_option("-a", "--alphabet_size", dest="alphabet_size", default = 100, type="int",
                     help="set the number of different character to ALPHA", metavar="ALPHA")

  parser.add_option("-s", "--string_size", dest="string_size", default=10*1000, type="int",
                     help="exploite a string of STRING random characters", metavar="STRING")

  parser.add_option("-p", "--nb_part", dest="nb_part", default = 1, type="int",
                     help="split the text in NB_PART", metavar="NB_PART")

  parser.add_option("-r", "--nb_run", dest="nb_run", default=20, type="int",
                     help="exec NB_RUN run", metavar="NB_RUN")

  parser.add_option("-i", "--limit_run", dest="limit_run", default=0, type="int",
                     help="erase the LIMIT_RUN first and last runs for the computation of the mean", metavar="LIMIT_RUN")

  return parser

def run_atomic_light(len_str, len_alpha, nb_part, nb_run, extremum) :
  nb_different_motifs = []
  nb_occurs = []
  nb_occurs_avg = []
  nb_occurs_sd = []

  for _ in xrange(nb_run) :
    rstr = Rstr_max()
    rs = random_string(len_str,len_alpha)
    lp = cut_str(rs,nb_part)
    for substring in lp :
      rstr.add_str(substring)
    r = rstr.go()

    nb_different_motifs_run = len(r.keys())
    nb_different_motifs.append(nb_different_motifs_run)
    l_nb_occ = [nb for (_, nb) in r.keys()]
    sum_nb_occ = sum(l_nb_occ)
    nb_occurs_avg.append(float(sum_nb_occ) / nb_different_motifs_run)
    nb_occurs_sd.append(tm.standart_deviation(l_nb_occ))
    nb_occurs.append(sum_nb_occ)

  if extremum > 0 :
    nb_different_motifs.sort()
    nb_different_motifs = nb_different_motifs[extremum:-extremum]
    nb_occurs.sort()
    nb_occurs = nb_occurs[extremum:-extremum]
    nb_occurs_avg.sort()
    nb_occurs_avg = nb_occurs[extremum:-extremum]

#  sd_motifs = tm.standart_deviation(nb_different_motifs)
#  sd_occurs = tm.standart_deviation(nb_occurs)

  moy = sum(nb_different_motifs) / len(nb_different_motifs)
  moy_occur = sum(nb_occurs) / len(nb_occurs)
  avg_occur = sum(nb_occurs_avg) / len(nb_occurs_avg)
  sd_occur = sum(nb_occurs_sd) / len(nb_occurs_sd)
#  return moy, moy_occur, avg_occur, sd_motifs, sd_occurs, dic_occ_len, dic_mot_len
  return moy, moy_occur, avg_occur, sd_occur


def run_atomic(len_str, len_alpha, nb_part, nb_run, extremum) :
  nb_different_motifs = []
  nb_occurs = []
  nb_occurs_avg = []
  nb_occurs_sd = []
  stat_alpha = []

  dic_zipf = {}
  dic_occ_len= {}
  dic_mot_len= {}

  for _ in xrange(nb_run) :
    rstr = Rstr_max()
    rs = random_string(len_str,len_alpha)
    lp = cut_str(rs,nb_part)
    for substring in lp :
      rstr.add_str(substring)
    r = rstr.go()

    list_zipf = []

    cpt = 0
    for (_,nb),(l,_) in r.iteritems() :
      if l not in dic_occ_len :
        dic_occ_len[l] = 0.
      if l not in dic_mot_len : 
        dic_mot_len[l] = 0.
      dic_occ_len[l] += float(nb) / nb_run
      dic_mot_len[l] += 1. / nb_run
      list_zipf.append(nb)
      cpt += 1

    list_zipf.sort()
    for i in xrange(1,cpt+1) :
      val = list_zipf[-i]
      if i not in dic_zipf :
        dic_zipf[i] = 0.
      dic_zipf[i] += float(val) / nb_run

    nb_different_motifs_run = len(r.keys())
    nb_different_motifs.append(nb_different_motifs_run)
    l_nb_occ = [nb for (_, nb) in r.keys()]
    sum_nb_occ = sum(l_nb_occ)
    nb_occurs_avg.append(float(sum_nb_occ) / nb_different_motifs_run)
    nb_occurs_sd.append(tm.standart_deviation(l_nb_occ))
    nb_occurs.append(sum_nb_occ)

  if extremum > 0 :
    nb_different_motifs.sort()
    nb_different_motifs = nb_different_motifs[extremum:-extremum]
    nb_occurs.sort()
    nb_occurs = nb_occurs[extremum:-extremum]
    nb_occurs_avg.sort()
    nb_occurs_avg = nb_occurs[extremum:-extremum]

#  sd_motifs = tm.standart_deviation(nb_different_motifs)
#  sd_occurs = tm.standart_deviation(nb_occurs)

  moy = sum(nb_different_motifs) / len(nb_different_motifs)
  moy_occur = sum(nb_occurs) / len(nb_occurs)
  avg_occur = sum(nb_occurs_avg) / len(nb_occurs_avg)
  sd_occur = sum(nb_occurs_sd) / len(nb_occurs_sd)
#  return moy, moy_occur, avg_occur, sd_motifs, sd_occurs, dic_occ_len, dic_mot_len
  return moy, moy_occur, avg_occur, sd_occur, dic_occ_len, dic_mot_len, dic_zipf



def run(len_str, len_alpha, nb_part, nb_run, extremum) :
  nb_different_motifs = []
  nb_occurs = []
  nb_occurs_avg = []
  stat_alpha = []
  dic_occ_len= {}
  dic_mot_len= {}

  for _ in xrange(nb_run) :
    rstr = Rstr_max()
    rs = random_string(len_str,len_alpha)
    lp = cut_str(rs,nb_part)
    for substring in lp :
      rstr.add_str(substring)
    r = rstr.go()

    for (_,nb),(l,_) in r.iteritems() :
      if l not in dic_occ_len :
        dic_occ_len[l] = 0.
      if l not in dic_mot_len : 
        dic_mot_len[l] = 0.
      dic_occ_len[l] += float(nb)/nb_run
      dic_mot_len[l] += 1./nb_run

    nb_different_motifs_run = len(r.keys())
    nb_different_motifs.append(nb_different_motifs_run)
    sum_nb_occ = sum([nb for (_, nb) in r.keys()])
    nb_occurs_avg.append(float(sum_nb_occ) / nb_different_motifs_run)
    nb_occurs.append(sum_nb_occ)

  if extremum > 0 :
    nb_different_motifs.sort()
    nb_different_motifs = nb_different_motifs[extremum:-extremum]
    nb_occurs.sort()
    nb_occurs = nb_occurs[extremum:-extremum]
    nb_occurs_avg.sort()
    nb_occurs_avg = nb_occurs[extremum:-extremum]

#  sd_motifs = tm.standart_deviation(nb_different_motifs)
#  sd_occurs = tm.standart_deviation(nb_occurs)

  moy = sum(nb_different_motifs) / len(nb_different_motifs)
  moy_occur = sum(nb_occurs) / len(nb_occurs)
  avg_occur = sum(nb_occurs_avg) / len(nb_occurs_avg)
#  return moy, moy_occur, avg_occur, sd_motifs, sd_occurs, dic_occ_len, dic_mot_len
  return moy, moy_occur, avg_occur, dic_occ_len, dic_mot_len

def random_string(n, l) :
#  r = array.array('u',[unicode('a','utf-8')]*n)
  r = []
  start = 20
  for i in xrange(n) :
    r.append(unichr(random.randint(start,start+l-1)))
#    r[i] = unichr(random.randint(2,2+l))
  return ''.join(r)

def urandom_string(n,l) :
  r = array.array('u',[unicode('a','utf-8')]*n)
  g = random.SystemRandom()
  for i in xrange(n) :
    r[i] = unichr(g.randint(2,2+l-1))
  return ''.join(r)


def athmospheric_random_string(n, l, p) :
  min_val, max_val = 2, 2 + l
  url = 'http://www.random.org/integers/?num=%s&min=%s&max=%s&col=1&base=10&format=plain&rnd=new'%(n, min_val, max_val) 
  r = array.array('u',[unicode('a','utf-8')]*n)
  u = urllib.urlopen(url, proxies = p)
  for i,v in enumerate(u.read().split()) :
    r[i] = unichr(int(v))
  return ''.join(r)


def list_int2list_char(l) :
  n = len(l)
  r = array.array('u',[unicode('a','utf-8')]*n)
  for i in l :
    r[i] = unichr(l+2)
  return ''.join(r)


def cut_str(s, nb_part) :
  l = len(s)
  step_size = l / nb_part
  current_limit, next_limit = 0, step_size
  list_part = []
  while current_limit < l :
    list_part.append(s[current_limit:next_limit])
    current_limit, next_limit = next_limit, next_limit + step_size
  return list_part

def nb_diff_char(s) :
  return len(set(s))

def alphabet_stat(s) :
  a = set(s)
  d = dict((c,0) for c in a)
  for c in s :
    d[c] += 1   
  l = [j for i,j in d.iteritems()]
  return l
