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
                #convert image from gif to png for use with cv2
                img = Image.open(self.imgPath + '.gif')
                new_im = Image.new("RGBA", img.size)
                new_im.paste(img)
                new_im.save(self.imgPath +'.png')
                self.imgPath += '.png'
                break
            else:
                continue
    
    def cropImage(self):
        if not re.search('.png', self.imgPath):
            raise GraphException('Image has not been converted')
        
        fullImage = cv2.imread(self.imgPath)
        centreBarY = self.getCentreBarPos()
        if centreBarY != -1:
            upperCrop = fullImage[25:centreBarY,108:488]
            lowerCrop = fullImage[centreBarY+2:232,108:488]

            return upperCrop,lowerCrop
        else:
            return fullImage[25:232,108:488],None


    
    def getCentreBarPos(self):
        img = cv2.imread(self.imgPath)
        img = img[:200,108:109]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([0,0,0])
        upper = np.array([200,200,200])
        mask = cv2.inRange(hsv,lower,upper)
        res = cv2.bitwise_and(img,img,mask=mask)
        for i,pixels in enumerate(res):
            if pixels[0,0] != 0:
                return i
        
        return -1
    
    def generateDataPointList(self,upperImage,lowerImage=None):
        lower = np.array([0,120,150])
        upper = np.array([255,255,255])
        listDataPoints = []
        #upper image data points
        hsvUpper = cv2.cvtColor(upperImage, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsvUpper,lower,upper)
        res = cv2.bitwise_and(upperImage,upperImage,mask=mask)
        for i,pixelList in enumerate(res):
            for j,pixel in enumerate(pixelList):
                if not all(v==0 for v in pixel):
                    if i > 0 and all(v==0 for v in res[i-1,j]):
                        listDataPoints.append([j,i])
                    elif j<len(pixelList)-1 and all(v==0 for v in res[i,j+1]):
                        listDataPoints.append([j,i])
                    elif j>0 and all(v==0 for v in res[i,j-1]):
                        listDataPoints.append([j,i])
        
        if lowerImage is not None:
            hsvLower = cv2.cvtColor(lowerImage, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsvLower,lower,upper)
            res = cv2.bitwise_and(lowerImage,lowerImage,mask=mask)
            for i,pixelList in enumerate(res):
                for j,pixel in enumerate(pixelList):
                    if not all(v==0 for v in pixel):
                        if i < len(res)-1 and all(v==0 for v in res[i-1,j]):
                            listDataPoints.append([j,i])
                        elif j<len(pixelList)-1 and all(v==0 for v in res[i,j+1]):
                            listDataPoints.append([j,i])
                        elif j>0 and all(v==0 for v in res[i,j-1]):
                            listDataPoints.append([j,i])

        return listDataPoints
    
    def sortDataPointList(self, dataPoints):
        #using bubble sort
        while True:
            sorted = True
            for i,point in enumerate(dataPoints):
                if i+1 < len(dataPoints) and point[0] > dataPoints[i+1][0]:
                    sorted = False
                    dataPoints[i], dataPoints[i+1] = dataPoints[i+1], dataPoints[i]
            if sorted:
                break

        return dataPoints

if __name__ == '__main__':
    gde = GraphDataExtractor('Amazon', 'amzn')
    #gde.pullGraphFromSite()
    gde.imgPath += '.png'
    u,l = gde.cropImage()
    data = gde.generateDataPointList(u,l)
    data = gde.sortDataPointList(data)
    print('{}'.format(data))