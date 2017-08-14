# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 18:27:34 2017

@author: Declan
"""
import sys

sys.path.insert(0,'../C-Modules/ArticleSearch')
import ArticleSearch
import ctypes

link = "hr\"1234\""
print(type(link))
res = ArticleSearch.clean_link_string(link)

print(res)
