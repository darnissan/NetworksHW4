import argparse
import sys
import random
import queue
class Request:
    def __init__(self, arrivalTime):
        self.arrivalTime = arrivalTime
        self.serviceTime = 0
        self.serviceStartTime = 0
        self.serviceEndTime = 0
        self.waitTime = 0
        self.lifeTime = 0
    
    
    
class Server:
    def __init__(self, rate,maxQueueSize):
        self.rate = rate
        self.queue = queue.Queue(maxQueueSize)
        self.maxQueueSize = maxQueueSize
    def addRequest(self):
        if self.queue.full():
            return False
        else:
            self.queue.put(1)
            return True
    def service(self):
        sum=0
        while not self.queue.empty() and sum < self.rate:
            sum += 1
            self.queue.get()
        return sum

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
            currentRequestNum += self.requestsRate
            sumRequestsAllTimes += currentRequestNum
            results = []
            for rqst in range(self.requestsRate):
                chosenServer=random.choices(list(range(len(self.probabilities))),weights=self.probabilities) # note servers are indices from n to len(probabilities)-1
                if servers[chosenServer].addRequest():
                    pass
                else:
                    thrownOut += 1
                    currentRequestNum -= 1
            for srv in servers:
                requestsServed= srv.service()
                currentRequestNum -= requestsServed
                receivedService += requestsServed   
        
        
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