#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from optparse import OptionParser
import sys
import re

def opt_parser_pyplot():
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="filein", default = "out.js",
                     help="Write report from FILE", metavar="FILE")
  parser.add_option("-o", "--output_file", dest="fileout", default = "bench.png",
                     help="Write report to FILEOUT (default)", metavar="FILEOUT")
  return parser


p = opt_parser_pyplot()
(opt_options, opt_args) = p.parse_args(sys.argv[1:])

r = open(opt_options.filein,'r').read()
js_plot = eval(r)

name_legend = []

for k,info in js_plot.iteritems() :
  if re.search('^global_',str(k)) :
    continue
  name_legend.append(info['name_legend'])
  plt.plot(info['list_x'], info['list_y'], info['style_plot'])

plt.xlabel(js_plot['global_x'])
plt.ylabel(js_plot['global_y'])
plt.legend(list(name_legend), 'upper left', shadow = False)
plt.savefig(opt_options.fileout)


