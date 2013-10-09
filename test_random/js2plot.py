#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from optparse import OptionParser
import sys
import re
import os

def opt_parser_pyplot():
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="filein", default = "",
                     help="Write report from FILE", metavar="FILE")
  parser.add_option("-o", "--output_file", dest="fileout", default = "",
                     help="Write report to FILEOUT (default)", metavar="FILEOUT")
  return parser

p = opt_parser_pyplot()
(opt_options, opt_args) = p.parse_args(sys.argv[1:])

def get_out_filename(in_filename) :
  out = os.path.split(in_filename)
  filename = out[-1]
  s = "%s.%s"%("".join(filename.split('.')[:-1]),'png')
  out_filename = os.path.join("".join(out[:-1]),s)
  return out_filename

for path_file in opt_args :
  r = open(path_file,'r').read()
  js_plot = eval(r)
  name_legend = []

  for k,info in js_plot.iteritems() :
    if re.search('^global_',str(k)) :
      continue
    name_legend.append(info['name_legend'])
#    plt.plot(info['list_x'], info['list_y'], info['style_plot'])
    plt.plot(info['list_x'], info['list_y'], 'b-')

  plt.xlabel(js_plot['global_x'])
  plt.ylabel(js_plot['global_y'])
  plt.legend(list(name_legend), 'upper right', shadow = False)
  out_filename = get_out_filename(path_file)
  plt.savefig(out_filename)
  print '>> %s'%(out_filename)
  plt.clf()
