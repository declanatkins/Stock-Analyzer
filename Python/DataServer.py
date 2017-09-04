'''
    Author: Declan Atkins
    Last Changed: 30/08/17
    
    This program runs the data side of the server
    it doesn't serve any pages it just interacts 
    with the file system and creates the json files
    that the web server passes to the browser
'''

import threading
import queue
from ModelHandler import Company
from ModelHandler import KeywordException
from ArticleHandler import ArticlePuller
from ArticleHandler import KeywordExtractor
from GraphHandler import GraphDataExtractor

class companiesReadyInputData:

    __instances = []
    @staticmethod
    def getInstance(name):
        for instance in __instances:
            if instance.name == name:
                return instance
        else:
            new = companiesReadyData(name)
            __instances.append(new)
            return new
    
    @staticmethod
    def destroyInstance(name):
        for instance in __instances:
            if instance.name == name:
                __instances.remove(instance)
                break
    
    def __init__(self, name):
        self.name = name
        self.values = None
        self.articles = None
        self.keywords = None

class DataServer:

    def __init__(self, companiesList):
        self.companiesList = companiesList
        for company in self.companiesList:
            companiesReadyInputData.getInstance(compay.name)
        self.graphThread = threading.Thread(target=self.graphManging)
        self.articleThread = threading.Thread(target=self.articleManaging)
        self.keywordThread = threading.Thread(target=self.keywordManaging)
        self.modelThread = threading.Thread(target=self.modelManaging)
        self.graphThread.start()
        self.articleThread.start()
        self.keywordThread.start()
        self.modelThread.start()

    def performGraphOperations(company):
        gde = GraphDataExtractor(company.name, company.abbrv)
        gde.pullGraphFromSite()
        upper, lower, centreBarY = gde.cropImage()
        dataList = gde.generateDataPointList(upper,lower,centreBarY)
        dataList = gde.sortDataPointList(dataList)
        val1,val2,val2Pos = gde.findValueIndicators()
        actualValuesList = gde.applyValuing(dataList,val1,val2,val2Pos)
        return actualValuesList

    def getArticleList(company):
        ap = ArticlePuller(company.name)
        html = ap.pullSearchPage()
        links = ap.searchForLinks(html)
        articleList = ap.pullArticles(links)
        return articleList

    def performKeywordSearch

if __name__ == '__main__':
    CompanyList = []
    with open('../Data/CompanyList.txt', 'r') as f:
        for line in f:
            splitStr = line.split()
            CompanyList.append(Company(splitStr[0], splitStr[1]))
    
    for company in CompanyList:
        values = performGraphOperations(company)
        articles = getArticleList(company)




