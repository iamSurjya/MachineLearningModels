import random, pylab, numpy

class tempData(object):
    def __init__(self,s):
        info=s.split(',')
        self.high=float(info[1])
        self.year=int(info[2][0:4])
    def getHigh(self):
        return self.high
    def getYear(self):
        return self.year

def getTempData():
    inFile=open('/Users/surajchoudhary/Documents/temperatures.csv')
    data=[]
    for l in inFile:
        data.append(tempData(l))
    return data
def getYearlyMeans(data):
    years={}
    for d in data:
        try:
            years[d.getYear()].append(d.getHigh())
        except:
            years[d.getYear()]=[d.getHigh()]
    for y in years:
        years[y]=sum(years[y])/len(years[y])
    return years

data=getTempData()
years=getYearlyMeans(data)
xVals,yVals=[],[]
for e in years:
    xVals.append(e)
    yVals.append(years[e])
pylab.plot(xVals,yVals)
pylab.xlabel('Year')
pylab.ylabel('Mean daily High(C)')
pylab.title('Select US City')
pylab.show()

numSubsets=10 #no of trials
dimensions=(1,2,3,4) #order of polynomials i.e models
rSquares={}
for d in dimensions:
    rSquares[d]=[]

def splitData(xVals,yVals):
    toTrain=random.sample(range(len(xVals)),len(yVals)//2)
    trainX,trainY,testX,testY=[],[],[],[]
    for i in range(len(xVals)):
        if i in toTrain:
            trainX.append(xVals[i])
            trainY.append(yVals[i])
        else:
            testX.append(xVals[i])
            testY.append(yVals[i])
    return trainX,trainY,testX,testY

def rSquared(observed, predicted):
    error = ((predicted - observed)**2).sum()
    meanError = error/len(observed)
    return 1 - (meanError/numpy.var(observed))

#Train,Test and Report
for f in range(numSubsets):
    trainX,trainY,testX,testY=splitData(xVals,yVals)
    for d in dimensions:
        model=pylab.polyfit(trainX,trainY,d)
        estYvals=pylab.polyval(model,testX)
        rSquares[d].append(rSquared(testY,estYvals))

print('Mean R-Squares for test data')
for d in dimensions:
    mean=round(sum(rSquares[d])/len(rSquares[d]),4)
    sd=round(numpy.std(rSquares[d]),4)
    print('For dimensions ',d,'Mean= ',mean,'SD=',sd)
