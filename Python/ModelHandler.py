import sys

sys.path.append("../C-Modules/ModelOperations")
import ModelOperations
import os

class KeywordException(Exception):
    pass

class Company:

    def __init__(self,name, abbrv):
        self.name = name
        self.abbrv = abbrv
        self.currentKeywordSet = ""
    
    def updateKeywordSet(self,currSet):
        if currSet not in os.listdir('../Data/'+ self.name + '/'):
            os.mkdir('../Data/' + self.name + '/' + currSet)
        self.currentKeywordSet = currSet

    def getPredictedVals(self):
        self.testKeywordError()
        self.predictedVals = ModelOperations.get_predicted_values(self.name, self.currentKeywordSet)
        return self.predictedVals
    
    def updateVals(self,listVals):
        self.testKeywordError()
        arr = ModelOperations.doubleArray(len(listVals))
        for i,val in enumerate(listVals):
            arr[i] = val
        ModelOperations.add_values(arr, len(listVals), self.name, self.currentKeywordSet)

    def getNextPredictedValue(self):
        self.testKeywordError()
        return ModelOperations.make_single_prediction_EXTERNAL(self.name,self.currentKeywordSet)

    def testKeywordError(self):
        if self.currentKeywordSet not in os.listdir('../Data/'+ self.name + '/'):
            raise KeywordException('Not a valid keyword set')

