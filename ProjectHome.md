# py-rstr-max : detection of all maximal repeats in strings, a python implementation #
  * [What does it look for?](http://code.google.com/p/py-rstr-max/#What_does_look_for?)
  * [Usage](http://code.google.com/p/py-rstr-max/#Usage)
  * [Bench py-rstr-max please](http://code.google.com/p/py-rstr-max/#Bench_py-rstr-max_please)
  * [Have fun with py-rstr-max](http://code.google.com/p/py-rstr-max/#Have_fun_with_py-rstr-max)
  * [py-rstr-max formally](http://code.google.com/p/py-rstr-max/#py-rstr-max_formally)
  * [See also](http://code.google.com/p/py-rstr-max/#See_also)

## What does it look for? ##

This implementation allows the detection, in linear time, of all the maximal repeats in one, or more, strings.

The complete extraction is done in quasi-linear time |n + z| where z is the number of maximal repeats in S. This implementation uses the computation of suffix array in linear time implemented in the [pysuffix project](http://code.google.com/p/pysuffix/)

The longest common prefix computation used is described in this paper http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.118.8221 and is included in the last version of [pysuffix project](http://code.google.com/p/pysuffix/)

Maximal repeats are also called non-gapped motif (http://www.springerlink.com/content/7215807755758m35/ Structural Analysis of Gapped Motifs of a String, Esko Ukkonen, 2007).

## Usage ##

Just go to the svn version ; or download the last version http://code.google.com/p/py-rstr-max/downloads/list

```
user@machine: tar -xvzf py-rstr-max.tar.gz
user@machine: cd py-rstr-max
user@machine: python rstr_max.test.py
```
## Inside rstr\_max.test.py (4.0) ##

Feed the process, here the string 'tititoto'

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools_karkkainen_sanders import *
from rstr_max import *

str1 = "tototiti"

str1_unicode = unicode(str1,'utf-8','replace')

rstr = Rstr_max()
rstr.add_str(str1_unicode) #str1
r = rstr.go()
```

Explore the results :
```
for (offset_end, nb), (l, start_plage) in r.iteritems():
  ss = rstr.global_suffix[offset_end-l:offset_end]
  id_chaine = rstr.idxString[offset_end-1]
  s = rstr.array_str[id_chaine]
  print '[%s] %d'%(ss.encode('utf-8'), nb)
  for o in range(start_plage, start_plage + nb) :
    offset_global = rstr.res[o]
    offset = rstr.idxPos[offset_global]
    id_str = rstr.idxString[offset_global]
    print '   (%i, %i)'%(offset, id_str)
```

Will print :
```
[t] 4
   (6, 0)
   (4, 0)
   (2, 0)
   (0, 0)
[tot] 2
   (2, 0)
   (0, 0)
[ti] 2
   (6, 0)
   (4, 0)
```

## Bench py-rstr-max please ##

Tests are done with a 2.4 Ghz core. Please, use **PyPy**.

<table>
<blockquote><tr><td>
<blockquote><img src='http://users.info.unicaen.fr/~rbrixtel/img_svn/bench_py_rstr.png' alt='bench_rstr' width='375' />
</blockquote></td><td>
<blockquote><img src='http://users.info.unicaen.fr/~rbrixtel/img_svn/bench_pypy_rstr.png' alt='bench_rstr_pypy' width='375' />
</blockquote></td></tr>
<tr><td align='center'>cPython</td><td align='center'>PyPy 1.6</td></tr>
</table></blockquote>

## Have fun with py-rstr-max ##

If you feel the fun of the Zipf's law, you will appreciate rstr\_max.zipf.py. This script show you how simple is the computation of the rank / freq. ratio (see bellow with log. scale).

<table><tr><td>
<pre><code>r = rstr.go()<br>
l = r.keys()<br>
<br>
def cmpval(x,y):<br>
  return y[1] - x[1]<br>
<br>
l.sort(cmpval)<br>
list_x = [math.log(elt[1]) for elt in l]<br>
list_y = [math.log(i) for i in range(1, len(list_x)+1)]<br>
<br>
plt.plot(list_x, list_y, 'r-')<br>
filename = 'zipf_rstr.png'<br>
plt.xlabel('log(rank)')<br>
plt.ylabel('log(freq.)')<br>
plt.savefig(filename)<br>
</code></pre>
</td>
<td>
<img src='http://users.info.unicaen.fr/~rbrixtel/img_svn/zipf_rstr.png' alt='bench_rstr' width='350' />
</td></tr></table>

## py-rstr-max formally ##

  * Let S a string of lenght ''n'' over a finite alphabet Σ.
  * S<sub>i</sub> refer to the i-th character of S.
  * S<sub>i..j</sub> refers to a substring of S starting at the position i and ending at position j.

  * Each position 0 ≤ i < n represents a unique suffix S<sub>i..n-1</sub> of S.
  * LC<sub>i</sub> refers to the Left Context of a suffix i. We note £ the special left context LC<sub>0</sub>.
  * We note with the special symbol $ the character S<sub>n</sub>.

A triple  (p<sub>1</sub> , p<sub>2</sub> , l) is called repeat in S iff :
  1. (p<sub>1</sub>+l-1 < n) ∧ (p<sub>2</sub>+l-1 < n) ∧ p<sub>1</sub> ≠ p<sub>2</sub>
  1. S<sub>p1..(p2+l-1)</sub> = S<sub>p2..(p2+l-1)</sub>

  * A repeat is called _Left Maximal_ if LC<sub>p1</sub> ≠ LC<sub>p1</sub> ∨ LC<sub>p1</sub> = £ ;
  * A repeat is called _Right Maximal_ if S<sub>p1..(p1+l)</sub> ≠ S<sub>p2..(p2+l)</sub> ∨ S<sub>p1..(p1+l)</sub> = $ ;
  * A repeat is _Maximal_ if it is _Left Maximal_ and _Right Maximal_ .

This implementation extracts all the _Maximal repeats_ in a string S. This is allowed by :
  * computing the suffix array of S
  * computing the longest common prefix of each suffix (ie: computing the augmented suffix array)
  * filtering each suffixes strictly included in an other.

## See also ##

  * [pysuffix project](http://code.google.com/p/pysuffix/)
  * [phpsuffix project](http://code.google.com/p/phpsuffix/)
  * [php-rstr-max project](http://code.google.com/p/php-rstr-max/)

### And also ###

  * [http://pyhtmllist.sourceforge.net/ : pyhtmllist project](http://pyhtmllist.sourceforge.net/)
  * [http://pypy.org/download.html : PyPy project](http://pypy.org/download.html)