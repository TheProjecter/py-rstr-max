#!/usr/bin/env python
# -*- coding: utf-8 -*-

#tri des caractères utilisés dans une chaîne
def lst_char(str_unicode):
  lst_ch = list(set(str_unicode))
  lst_ch.sort()
  return lst_ch

def leq2(a1,a2,b1,b2) :
  return (a1 < b1 or (a1 == b1 and a2 <= b2))

def leq3(a1,a2,a3,b1,b2,b3) :
  return (a1 < b1 or (a1 == b1 and leq2(a2,a3,b2,b3)))

def simple_kark_sort(s):
  print repr(s)
  n = len(s)
  s += (unichr(1) * 3)
  SA = [0 for _ in s]
  alpha = sorted(set(s))
  kark_sort(s, SA, n, alpha)
  return SA

def kark_sort(s, SA, n, alpha) :
  n0 = int((n+2)/3)
  n1 = int((n+1)/3)
  n2 = int(n/3)
  n02 = n0 + n2
  SA12 = [0]*(n02+3)
  SA0 = [0]*n0 
  s12 = []

## begin modification (from : htmllist)##
#  max = n + n0 - n1
#  for i in range(max) :
#    if i % 3 != 0:
#      s12.append(i)
  s12 = [i for i in xrange(n + n0 - n1) if i % 3 != 0]
##end moditication

  s12.extend([0,0,0])
#  s_2 = s[2:]

  radixpass(s12, SA12, s[2:], n02, alpha)
  radixpass(SA12, s12, s[1:], n02, alpha)
  radixpass(s12, SA12, s, n02, alpha)
  
  name = 0
  c0, c1, c2 = -1, -1, -1
  array_name = [0]
  for i in xrange(n02) :
    if s[SA12[i]] != c0 or s[SA12[i]+1] != c1 or s[SA12[i]+2] != c2 :
      name += 1
      array_name.append(name)
      c0 = s[SA12[i]]
      c1 = s[SA12[i]+1]
      c2 = s[SA12[i]+2]
    if SA12[i] % 3 == 1 :
      s12[int(SA12[i]/3)] = name
    else :
      s12[int(SA12[i]/3) + n0] = name

  if name < n02 :
    kark_sort(s12, SA12,n02,array_name)
    for i in xrange(n02) : 
      s12[SA12[i]] = i+1
  else :
    for i in xrange(n02) : 
      SA12[s12[i]-1] = i

  s0 = []
  for i in xrange(n02) :
    if SA12[i] < n0 :
      s0.append(SA12[i]*3)

  radixpass(s0,SA0,s,n0,alpha)
  
  p = j = k = 0
  t = n0 - n1
  while k < n :
    if SA12[t] < n0 :
      i = SA12[t] * 3 + 1
    else :
      i = (SA12[t] - n0 ) * 3 + 2

    if p < len(SA0) :
      j = SA0[p]
    else :
      j = 0
 
    if SA12[t] < n0 :
      test = leq2(s[i], s12[SA12[t]+n0],s[j], s12[int(j/3)])
    else :
      test = leq3(s[i], s[i+1], s12[SA12[t]-n0+1], s[j], s[j+1], s12[int(j/3)+n0])  

    if(test) :
      SA[k] = i
      t += 1
      if t == n02 : 
        k += 1
        while p < n0 :
          SA[k] = SA0[p]
          p += 1
          k += 1
      
    else : 
      SA[k] = j
      p += 1
      if p == n0 :
        k += 1
        while t < n02 :
          if SA12[t] < n0 :
            SA[k] = (SA12[t] * 3) + 1
          else :
            SA[k] = ((SA12[t] - n0) * 3) + 2
          t += 1
          k += 1
    k += 1


def radixpass(a, b, r, n, k) :
  f_ord = ord(str(k[0])) - 1
  f_new = unichr(f_ord)

  c = {f_new : 0}
  liste = [f_new]
  for lettre in k :
    liste.append(lettre)
    c[lettre] = 0

  for i in xrange(n) :
    c[r[a[i]]] += 1
  
  somme = 0 
  for lettre in liste :
    freq , c[lettre] = c[lettre] , somme
    somme += freq

  for i in xrange(n) :
    b[c[r[a[i]]]] = a[i]
    c[r[a[i]]] += 1

  return b

if (__name__ == '__main__') :
  print "tools.py"
