'''
    Author: Declan Atkins
    Last Changed: 30/08/17
    
    This program runs the data side of the server
    it doesn't serve any pages it just interacts 
    with the file system and creates the json files
    that the web server passes to the browser
'''

import threading

from ModelHandler import Company
from ModelHandler import KeywordException
from ArticleHandler import ArticlePuller

if __name__ == '__main__':
    CompanyList = []
    with open('../Data/CompanyList.txt', 'r') as f:
        for line in f:
            splitStr = line.split()
            CompanyList.append(Company(splitStr[0], splitStr[1]))
    
    for company in CompanyList:
        ap = ArticlePuller(company.name)
        h = ap.pullSearchPage()
        l = ap.searchForLinks(h)
        a = ap.pullArticles(l)
        print('{}'.format(a))



