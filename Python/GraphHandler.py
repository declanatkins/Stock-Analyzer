"""
Author Declan Atkins
Last Changed: 24/08/17

This module is used to parse the data from graphs 
that are taken in.

"""
import re
import cv2
import numpy as np
from urllib import request
from newspaper import Article



class GraphException(Exception):
    pass 

class GraphDataExtractor:

    def __init__(self, companyName,companyAbbr):
        self.abbrv = companyAbbr
        self.name = companyName
        self.imgPath = '../Data/Graphs/' + self.name + '.jpg'

    def pullGraphFromSite(self):
        url = 'http://www.nasdaq.com/symbol/' + self.abbrv + '/stock-chart?intraday=on&timeframe=intra'
        
        try:
            graphWebPage = Article(url)
            graphWebPage.download()
            htmlStr = graphWebPage.html
        except newspaper.ArticleException:
            raise GraphException('Couldnt download webpage') 

        while True:
            if not re.search('<img', htmlStr):
                raise GraphException('Chart not on page')
            pre,sep,block = htmlStr.partition('<img')
            img,sep,htmlStr = block.partition('>')

            if 'stock chart' in img:
                imgURL = re.search('\"(.+?)\"', img).group(1)
                with open(self.imgPath, 'wb') as imgFile:
                    imgFile.write(request.urlopen(imgURL).read())
                break
            else:
                continue
    
    def cropImage(self):
        import os
        print(os.getcwd())
        img = cv2.imread('C:/Users/Declan/Desktop/Stock-AnalyzerData/Graphs/amazon.jpg', 1)
        #img = cv2.imread(self.imgPath)
        cv2.imshow('precrop',img)
        #cv2.waitkey(0)
        #cropImg = img[70:30, 550:100]
        #cv2.imshow('cropped',cropImg)
        #cv2.waitkey(0)

if __name__ == '__main__':
    import os
    l = os.listdir('../data/graphs')
    print("{}".format(l))



