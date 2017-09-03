# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 18:27:34 2017

@author: Declan
"""

import re
from newspaper import Article
from newspaper import ArticleException

class ArticlePuller:

    def __init__(self,companyName):
        self.name = companyName

    def pullSearchPage(self):
        url = 'https://www.google.ie/search?q=' + self.name + '&tbm=nws'
        searchPage = Article(url)
        searchPage.download()
        return searchPage.html
    
    def searchForLinks(self,html):
        links = []
        #headers,sep,html = html.partition('class=\"mw\"')
        while True:
            pre,sep,block = html.partition('class=\"g\"')
            if sep:
                pre,sep,link = block.partition('href=\"')
                link,sep,html = link.partition('\"')
                link = link.replace('/url?q=', '')
                links.append(link)
            else:
                print("2")
                break
        return links

    def pullArticles(self,links):
        articles = []
        for link in links:
            a = Article(link)
            try:
                print(link)
                a.download()
                a.parse()
                articles.append(a.text)
            except ArticleException as e:
                print('{}'.format(e))
                pass
        
        return articles

class KeywordExtractor():

    def __init__(self,article):
        self.article = article
    
    def loadKeywordSets(self):
        keywords = dict()
        with open('../Data/KeywordSets.dat', 'r') as keywordFile:
            for line in keywordFile:
                line = line.split()
                kewords[line[0]] = [keyword for keyword in line[1:]]

        self.keywordDict = keywords
    
    def searchForKeywordMatch(self):
        matches = dict()
        for key in self.keywordDict:
            matches[key] = 0
        
        for word in self.article.split():
            for key in self.keywordDict:
                if word in self.keywordDict[key]:
                    matches[key] += 1
                    break
        
        return matches





