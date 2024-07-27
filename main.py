import argparse
import sys
import random
import queue


    

class Request:
    def __init__(self, arrivalTime):
        self.arrivalTime = arrivalTime
        self.serviceEndTime = 0
        self.waitTime = 0
        self.lifeTime = 0
    def getArirvalTime(self):
        return self.arrivalTime
    
    
    
class Server:
    def __init__(self, rate,maxQueueSize):
        self.rate = rate
        self.queue = queue.Queue(maxQueueSize)
        self.maxQueueSize = maxQueueSize
        self.lastRequestTime = 0
        self.queueMaxSize=0
    def addRequest(self, request):
        if self.queue.full():
            return False
        else:
            self.queue.put(request)
            return True
        
    def service(self):
        currentRequest = self.queue.get()
        currentRequest.serviceEndTime = currentRequest.arrivalTime+self.lastRequestTime+ 1/self.rate
        self.lastRequestTime = currentRequest.serviceEndTime

class Simulator :
    def __init__(self , simulatorTimeOut,numOfServer, probabilities, requestsRate, queues, serverRates) :
        self.timeOut = simulatorTimeOut
        self.numOfServers=numOfServer
        self.probabilities = probabilities
        self.requestsRate = requestsRate
        self.queues = queues
        self.serverRates = serverRates
        self.numOfSuccessReqA=0
        self.numOfRejectedReqB=0
        self.timeOfLastSuccessReq=0
        self.avgWaitTimeOfSuccessReq=0
        self.AvgLifeTimeOfReq=0
    
      
        
        
    def run(self):
        sumRequestsAllTimes=0
        currentRequestNum= 0
        receivedService= 0
        thrownOut= 0
        lastRequest= 0
        servers=[]
        for serv in range(self.numOfServers):
            servers += Server(self.requestsRate[serv], self.queues[serv])
        for t in range(self.timeOut):
            for CurReqIndex in range(self.requestsRate):
                req= Request(t+CurReqIndex/self.requestsRate)
                #availableRequets+=
                chosenServer=random.choices(list(range(len(self.probabilities))),weights=self.probabilities) # note servers are indices from n to len(probabilities)-1
                if servers[chosenServer].addRequest(req):
                    pass
                else:
                    currentRequestNum -= 1
        for srv in servers:
            serverTime=0
            firstRequest=srv.queue.get()
            while serverTime <  self.timeOut: 
                serverTime += 1/srv.rate
                if serverTime == firstRequest.arrivalTime:
                    receivedService += 1
                    currentRequestNum -= 1
                
            
            currentRequestNum += self.requestsRate
            sumRequestsAllTimes += currentRequestNum  
        
        
def main(argc):
    SimulatorTimeout = int(argc[0])
    numberOfServers = int(argc[1] )
    ServersProbabilities = [float(arg) for arg in argc[2:2+numberOfServers]]
    RequestsRate = int(argc[2+numberOfServers])
    Queues = [int(arg) for arg in argc[3+numberOfServers:3+2*numberOfServers]]
    ServersRates = [int(arg) for arg in argc[3+2*numberOfServers:]]
    Shimon = Simulator(SimulatorTimeout,numberOfServers, ServersProbabilities, RequestsRate, Queues, ServersRates)
    Shimon.run()




if __name__ == "__main__":
    breakpoint()
    main(sys.argv[1:])   