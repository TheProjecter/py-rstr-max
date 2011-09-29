#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from rstr_max import Rstr_max

class Test_rstrmax:
  def setUp(self):
    self.s = self.getString()
    self.rstr = Rstr_max()
    self.rstr.add_str(self.s)

  def test_rstr_max(self) :
    r = self.rstr.go()
    for ((idStr, end), nb), (l, start_plage) in r.iteritems():
      ss = self.rstr.array_str[idStr][end-l:end]
      s = self.rstr.array_str[idStr]
      idx = 0
      for i in xrange(nb):
        idx = s.index(ss, idx) + 1
#      except ValueError, e:
#        print "+++", ss, end, i, nb
#      try:
      self.assertRaises(ValueError, s.index, ss, idx)
#        print "***", ss, end, i, nb
#      except ValueError, e:
#        pass

  def test_left_maximality(self) :
    r = self.rstr.go()
    for ((idStr, end), nb), (l, start_plage) in r.iteritems():
      ss = self.rstr.array_str[idStr][end-l:end]
      s = self.rstr.array_str[idStr]
      set_left_char = set()
      for o in range(start_plage, start_plage + nb) :
        su = self.rstr.array_suffix[o]
        if(su[0] == 0) :
          char_left = "START_STR"
        else :
          char_left = self.rstr.array_str[su[1]][su[0]-1]
        set_left_char.add(char_left)
      if(len(set_left_char) == 1) :
        print
        print '*'*10
        print set_left_char
        print ss.encode('utf-8')
        print '*'*10
        print
      self.assertNotEqual(len(set_left_char), 1)

  def test_right_maximality(self) :
    r = self.rstr.go()
    for ((idStr, end), nb), (l, start_plage) in r.iteritems():
      ss = self.rstr.array_str[idStr][end-l:end]
      s = self.rstr.array_str[idStr]
      set_right_char = set()
      for o in range(start_plage, start_plage + nb) :
        su = self.rstr.array_suffix[o]
        ls = len(self.rstr.array_str[su[1]])
        if(su[0]+l == ls) :
          char_right = "END_STR"
        else :
          char_right = self.rstr.array_str[su[1]][su[0]+l]
        set_right_char.add(char_right)
      if(len(set_right_char) == 1) :
        print
        print '*'*10
        print set_right_char
        print ss.encode('utf-8')
        print '*'*10
        print
      self.assertNotEqual(len(set_right_char), 1)


class Test_rstrmax_test1(Test_rstrmax, unittest.TestCase):
  def getString(self):
    str1 = " u u"
    return unicode(str1,'utf-8','replace')

#class Test_rstrmax_otto(Test_rstrmax, unittest.TestCase):
#  def getString(self):
#    str1 = open('otto.txt','r').read()
#    return unicode(str1,'utf-8','replace')
   
#class iTest_rstrmax_python(Test_rstrmax, unittest.TestCase):
#  def getString(self):
#    str1 = open('Python.htm','r').read()
#    return unicode(str1,'utf-8','replace')[:1000]

class Test_rstrmax_a(Test_rstrmax, unittest.TestCase):
  def getString(self):
    return 'a'*50

class Test_rstrmax_tititoto(Test_rstrmax, unittest.TestCase):
  def getString(self):
    return 'tititoto'

class Test_rstrmax_toto(Test_rstrmax, unittest.TestCase):
  def getString(self):
    return 'toto'

#class iTest_rstrmax_art(Test_rstrmax, unittest.TestCase):
#  def getString(self):
#    str1 = open('002.art','r').read()
#    return unicode(str1,'utf-8','replace')

if (__name__ == '__main__') :
  unittest.main()

