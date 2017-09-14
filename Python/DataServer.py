'''
    Author: Declan Atkins
    Last Changed: 30/08/17
    
    This program runs the data side of the server
    it doesn't serve any pages it just interacts 
    with the file system and creates the json files
    that the web server passes to the browser
'''

import threading
import time
import datetime
import pandas as pd
from ModelHandler import Company
from ModelHandler import KeywordException
from ArticleHandler import ArticlePuller
from ArticleHandler import KeywordExtractor
from GraphHandler import GraphDataExtractor

class companiesReadyInputData:

    __instances = []
    @staticmethod
    def getInstance(name):
        for instance in companiesReadyInputData.__instances:
            if instance.name == name:
                return instance
        else:
            new = companiesReadyInputData(name)
            companiesReadyInputData.__instances.append(new)
            return new
    
    @staticmethod
    def destroyInstance(name):
        for instance in companiesReadyInputData.__instances:
            if instance.name == name:
                companiesReadyInputData.__instances.remove(instance)
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
            companiesReadyInputData.getInstance(company.name)
        self.inputThread = threading.Thread(target=self.inputManagement)
        self.outputThread = threading.Thread(target=self.outputManagement)
        self.inputThread.start()
        #self.outputThread.start()

    def inputManagement(self):
        self.graphThread = threading.Thread(target=self.graphManaging)
        self.articleThread = threading.Thread(target=self.articleManaging)
        self.keywordThread = threading.Thread(target=self.keywordManaging)
        self.modelThread = threading.Thread(target=self.modelManaging)
        while True:
            self.graphThread.start()
            self.articleThread.start()
            self.keywordThread.start()
            self.modelThread.start()
            break
            time.sleep(86400)

    def outputManagement(self):
        self.predictionThread = threading.Thread(target=self.predictionManaging)
        while True:
            self.predictionThread.start()
            time.sleep(86400)

    ##Thread Methods
    def predictionManaging(self):
        for company in self.companiesList:
            if company.currentKeywordSet == '':
                company.currentKeywordSet = 'Neutral'
            predictedVals = company.getPredictedVals()
            series = pd.Series(data = predictedVals,name='PredictedValue')
            frame = pd.DataFrame(series)
            frame.to_json('../FlaskServer/static/json/' + company.name +'.json')
            

    def graphManaging(self):
        for company in self.companiesList:
            self.performGraphOperations(company)
            print("Got Graphs")

    def articleManaging(self):
        for company in self.companiesList:
            self.getArticleList(company)
            print('got articles')
    
    def keywordManaging(self):
        companiesToDo = list(self.companiesList)
        while len(companiesToDo) > 0:
            for company in companiesToDo:
                instance = companiesReadyInputData.getInstance(company.name)
                if instance.articles is not None:
                    self.getKeywordSet(company)
                    companiesToDo.remove(company)
                    print('got keywords')
            time.sleep(5)

    def modelManaging(self):
        companiesToDo = list(self.companiesList)
        while len(companiesToDo) > 0:
            for company in companiesToDo:
                instance = companiesReadyInputData.getInstance(company.name)
                if instance.keywords is not None and instance.values is not None:
                    self.updateValues(company)
                    companiesToDo.remove(company)
            time.sleep(5)

    ##Queue Methods
    def performGraphOperations(self,company):
        gde = GraphDataExtractor(company.name, company.abbrv)
        gde.pullGraphFromSite()
        upper, lower, centreBarY = gde.cropImage()
        dataList = gde.generateDataPointList(upper,lower,centreBarY)
        dataList = gde.sortDataPointList(dataList)
        val1,val2,val2Pos = gde.findValueIndicators()
        actualValuesList = gde.applyValuing(dataList,val1,val2,val2Pos)
        instance = companiesReadyInputData.getInstance(company.name)
        instance.values = actualValuesList

    def getArticleList(self,company):
        ap = ArticlePuller(company.name)
        html = ap.pullSearchPage()
        links = ap.searchForLinks(html)
        articleList = ap.pullArticles(links)
        instance = companiesReadyInputData.getInstance(company.name)
        instance.articles = articleList

    def getKeywordSet(self,company):
        instance = companiesReadyInputData.getInstance(company.name)
        articles = instance.articles
        ke = KeywordExtractor(articles)
        ke.loadKeywordSets()
        matches = ke.searchForKeywordMatch()
        domSet = ke.getDominantKeywordSet(matches)
        instance = companiesReadyInputData.getInstance(company.name)
        instance.keywords = domSet
    
    def updateValues(self,company):
        instance = companiesReadyInputData.getInstance(company.name)
        vals = instance.values
        keywordSet = instance.keywords
        company.updateKeywordSet(keywordSet)
        company.updateVals(vals)
        print('finished ' + company.name)
        companiesReadyInputData.destroyInstance(company.name)


if __name__ == '__main__':
    CompanyList = []
    with open('../Data/CompanyList.txt', 'r') as f:
        for line in f:
            splitStr = line.split()
            CompanyList.append(Company(splitStr[0], splitStr[1]))
    
    DS = DataServer(CompanyList)




