# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 18:27:34 2017

@author: Declan
"""

import re
from newspaper import Article
from newspaper import ArticleException

class ArticlePuller:

    def __init__(self,companyName,companyAbbrv)
        self.name = companyName
        self.abbrv = companyAbbrv

    def pullSearchPage(self):
        url = 'https://www.google.ie/search?q=' + self.name + '&tbm=nws'
        searchPage = Article(url)
        searchPage.download()
        return searchPage.html
    
    def searchForLinks(self,html):
        links = []
        while True:
            pre,sep,block = html.partition('class=g')
            if sep:
                pre,sep,link = block.partition('href=\"')
                link,sep,html = block.partition('\"')
                links.append(link)
            else:
                break
        return links

    def pullArticles(self,links):
        articles = []
        for link in links:
            a = Article(link)
            try:
                a.download()
                a.parse()
                articles.append(a.text)
            except ArticleException:
                pass

class KeywordExtractor():
    

