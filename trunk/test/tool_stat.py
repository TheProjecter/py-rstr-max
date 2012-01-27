#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import array
import urllib
import os


def random_string(n, l) :
#  r = array.array('u',[unicode('a','utf-8')]*n)
  r = []
  for i in xrange(n) :
    r.append(unichr(random.randint(2,2+l-1)))
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
