"""
Author Declan Atkins
Last Changed: 24/08/17

This module is used to parse the data from graphs 
that are taken in.

"""
import re
import os
import cv2
import numpy as np
from urllib import request
from newspaper import Article,ArticleException
from PIL import Image
from matplotlib import pyplot as plt

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

            return upperCrop,lowerCrop,centreBarY
        else:
            return fullImage[25:232,108:488],None,0


    
    def getCentreBarPos(self):
        print(self.imgPath)
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
    
    def generateDataPointList(self,upperImage,lowerImage=None,barY=0):
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
                            listDataPoints.append([j,barY-25+i])
                        elif j<len(pixelList)-1 and all(v==0 for v in res[i,j+1]):
                            listDataPoints.append([j,barY-25+i])
                        elif j>0 and all(v==0 for v in res[i,j-1]):
                            listDataPoints.append([j,barY-25+i])

        return listDataPoints
    
    def sortDataPointList(self, dataPoints, barY=0):
        #using bubble sort
        while True:
            sorted = True
            for i,point in enumerate(dataPoints):
                if i+1 < len(dataPoints) and point[0] > dataPoints[i+1][0]:
                    sorted = False
                    dataPoints[i], dataPoints[i+1] = dataPoints[i+1], dataPoints[i]
                elif i+1 < len(dataPoints) and point[0] == dataPoints[i+1][0]:#for removing duplicates
                    sorted = False
                    if abs(point[1] - barY) > abs(dataPoints[i+1][1] - barY):
                        dataPoints.remove(point)
                    else:
                        dataPoints.remove(dataPoints[i+1])
                    break
            if sorted:
                break
            
        listVals = [207 - v[1] for v in dataPoints]

        return listVals

    def findValueIndicators(self, graph):
        block1 = graph[24:32, 640:690]
        secondPos = 0
        for i,pixel in enumerate(graph[60:200,641:642]):
            if pixel[0][0] == 232:
                secondPos = i+26
                break
        block2 = graph[secondPos+2:secondPos+8,640:690]
        block1 = self.blockToBWString(block1)
        block1 = self.valStringFromBlock(block1)
        block2 = self.blockToBWString(block2)
        block2 = self.valStringFromBlock(block2)
        
        return float(block1), float(block2), secondPos

    def blockToBWString(self,block):
        blockStr = []
        for pixelList in block:
            lineStr = ""
            for pixel in pixelList:
                if pixel[0] == 96:
                    lineStr += 'b'
                else:
                    lineStr += 'w'
            blockStr.append(lineStr)

        return blockStr

    
    def valStringFromBlock(self,block):
        ##These are the breakdowns of pixels in each number eg 0:
        #wbbbw
        #bwwwb
        #bwwwb
        #bwwwb
        #bwwwb
        #bwwwb
        #bwwwb
        #wbbbw
        #can test downwards on the image until the result is no longer ambiguous
        str0 = ["wbbbw","bwwwb","bwwwb","bwwwb","bwwwb","bwwwb","bwwwb","wbbbw"]
        str1 = ["wwbww","wbbww","bwbww","wwbww","wwbww","wwbww","wwbww","wwbww"]
        str2 = ["wbbbw","bwwwb","wwwwb","wwwwb","wwwbw","wwbww","wbwww","bbbbb"]
        str3 = ["wbbbw","bwwwb","wwwwb","wwbbw","wwwwb","wwwwb","bwwwb","wbbbw"]
        str4 = ["wwwbw","wwbbw","wbwbw","wbwbw","bwwbw","bbbbb","wwwbw","wwwbw"]
        str5 = ["wbbbb","wbwww","bwwww","bbbbw","wwwwb","wwwwb","bwwwb","wbbbw"]
        str6 = ["wbbbw","bwwwb","bwwww","bbbbw","bwwwb","bwwwb","bwwwb","wbbbw"]
        str7 = ["bbbbb","wwwbw","wwwbw","wwbww","wwbww","wbwww","wbwww","wbwww"]
        str8 = ["wbbbw","bwwwb","bwwwb","wbbbw","bwwwb","bwwwb","bwwwb","wbbbw"]
        str9 = ["wbbbw","bwwwb","bwwwb","bwwwb","wbbbb","wwwwb","bwwwb","wbbbw"]
        numbers = [str0,str1,str2,str3,str4,str5,str6,str7,str8,str9]

        valStr = ''
        i = 0
        while True:
            if i+5 >= len(block[0]):
                break
            else:
                potentialIndexes = []
                for j,string in enumerate(numbers):
                    if string[0] == block[0][i:i+5]:
                        potentialIndexes.append(j)
                
                if len(potentialIndexes) > 0:
                    k = 1
                    while len(potentialIndexes) > 0:
                        for index in potentialIndexes:
                            if not block[k][i:i+5] == numbers[index][k]:
                                potentialIndexes.remove(index)
                        
                        k+=1
                        if k > 7:
                            break 
                        if k > 2 and len(potentialIndexes) == 1:#checked enough to ensure accuracy
                            break 
                
                if len(potentialIndexes) == 0:
                    i+=1
                else:
                    valStr += str(potentialIndexes[0])
                    i+=5
                    #now test for .
                    if block[7][i:i+4] == 'wwbw':
                        valStr += '.'
                        i+=4

        return valStr
                    






if __name__ == '__main__':
    gde = GraphDataExtractor('Amazon', 'amzn')
    img = cv2.imread(gde.imgPath + '.png')
    gde.findValueIndicators(img)