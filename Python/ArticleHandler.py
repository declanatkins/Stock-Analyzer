# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 18:27:34 2017

@author: Declan
"""

from newspaper import Article

def pullHTMLFiles():
    
    fh = open("../data/CompanyList.txt")
    
    for line in fh:
        searchPage = "https://www.google.ie/search?q="+line+ "&safe=off&source=lnms&tbm=nws"
        a = Article(searchPage)
        a.download()
        
        
pullHTMLFiles()