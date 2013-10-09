#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

#repartition ::
#repartition[x] = y

def regression_lineaire_simple(rep) :
  """rep[x]=y"""
  n = len(rep)
  s_x, s_y, s_xy, s_x2, s_y2 = 0., 0., 0., 0., 0.
  for x in xrange(n) :
    y = rep[x]
    s_x += x
    s_y += y
    s_xy += x*y
    s_x2 += math.pow(x,2) 
    s_y2 += math.pow(y,2) 
  mx = s_x / float(n)
  my = s_y / float(n)
  covariance_xy = (s_xy/n) - (mx*my)
  variance_x, variance_y = 0., 0.
  for i in xrange(n) :
    variance_x += math.pow(i-mx, 2)
    variance_y += math.pow(rep[i]-my, 2)
  variance_x /= n
  variance_y /= n
  ecart_type_x = math.sqrt(math.fabs(variance_x))
  ecart_type_y = math.sqrt(math.fabs(variance_y))
  r = covariance_xy / (ecart_type_x * ecart_type_y)
  a = r * (ecart_type_y/ecart_type_x)
  b = my - (a*mx)

  return {'r':r, 'a':a, 'b':b}

#ecart type
def standart_deviation(rep) :
  n = len(rep)
  if n == 0 :
    return 0.
  moy = avg(rep)
  v = 0.
  for i in xrange(n) :
    v += math.pow(rep[i]-moy,2) 
  v /= n
  return math.sqrt(math.fabs(v))

#esperance
def expected_value(rep) :
  n = len(rep)
  s = sum(rep)
  e = 0.
  for i in xrange(n) :
    e += i * (float(rep[i]) / s)
  return e

#moyenne
def avg(rep) :
  return float(sum(rep))/len(rep)

# segmentation en n parties de même nombre d'éléments
def ntile(rep,n) :
  rep.sort()
  length = len(rep)
  nb = length / n
  s = 0
  res = []
  for i in xrange(n) :
    res.append(rep[s:s+nb])
    s += nb
  if s < length :
    for elt in rep[s:] :
      res[-1].append(elt)
  return res

def all_vals_between(rep, inf, sup) :
  return [v for v in rep if inf <= v <= sup]

def sublist_between(rep, list_frontier) :
  min_rep = min(rep)
  max_rep = max(rep)
  res = []
  for frontier in list_frontier :
    res.append([v for v in rep if min_rep <= v < frontier])
    min_rep = frontier
  res.append([v for v in rep if min_rep <= v <= max_rep])
  return res

def frontier_entangled_mean(rep, n):
  val_max = max(rep)
  val_min = min(rep)
  lst = [(val_min,val_max,n)]
  list_frontier = []
  while lst:
    inf,sup,n = lst.pop()
    m = avg(all_vals_between(rep, inf, sup))
    list_frontier.append(m)
    if n == 1:
        continue
    lst.append((inf,m,n-1))
    lst.append((m,sup,n-1))
  list_frontier.sort()
  return list_frontier
#  return sublist_between(rep, list_frontier)

