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
from newspaper import Article,ArticleException
from PIL import Image

class GraphException(Exception):
    pass 

class GraphDataExtractor:

    def __init__(self, companyName,companyAbbr):
        self.abbrv = companyAbbr
        self.name = companyName
        self.imgPath = '../Data/Graphs/' + self.name

    def pullGraphFromSite(self):
        url = 'http://www.nasdaq.com/symbol/' + self.abbrv + '/stock-chart?intraday=on&timeframe=intra'
        
        try:
            graphWebPage = Article(url)
            graphWebPage.download()
            htmlStr = graphWebPage.html
        except ArticleException:
            raise GraphException('Couldnt download webpage') 

        while True:
            if not re.search('<img', htmlStr):
                raise GraphException('Chart not on page')
            pre,sep,block = htmlStr.partition('<img')
            img,sep,htmlStr = block.partition('>')

            if 'stock chart' in img:
                imgURL = re.search('\"(.+?)\"', img).group(1)
                with open(self.imgPath + '.gif','wb') as imgFile:
                    imgFile.write(request.urlopen(imgURL).read())
                break
            else:
                continue
    
    def cropImage(self):
        img = Image.open(self.imgPath + '.gif')
        new_im = Image.new("RGBA", img.size)
        new_im.paste(img)
        new_im.save(self.imgPath +'.png')
        graph = cv2.imread(self.imgPath +'.png')
        print(graph)


if __name__ == '__main__':
    gde = GraphDataExtractor('Amazon', 'amzn')
    #gde.pullGraphFromSite()
    gde.cropImage()
