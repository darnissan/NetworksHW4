import argparse
import sys
import random
from collections import deque
import heapq as heqpq
import numpy as np
    

class Request:
    def __init__(self, arrivalTime):
        self.arrivalTime = arrivalTime
        self.serviceEndTime = 0
        self.waitTime = 0
        self.lifeTime = 0
        self.serviceTime=0
        self.chosenServer=0
    def getArirvalTime(self):
        return self.arrivalTime
    
    
    
class Server:
    def __init__(self, rate,maxQueueSize):
        self.rate = rate
        self.queue = deque(maxlen=maxQueueSize)
        self.maxQueueSize = maxQueueSize
        self.lastRequestTime = 0
        self.firstInLine=None
        
    def addRequest(self, request):
        if len(self.queue) == self.maxQueueSize:
            if(request.arrivalTime < self.queue[0].serviceEndTime):
                return False
            while self.queue and request.arrivalTime >= self.queue[0].serviceEndTime:
                self.queue.pop()
        self.queue.append(request)
        request.serviceEndTime=request.arrivalTime
        for i in range(len(self.queue)):
            request.serviceEndTime+=self.queue[i].serviceTime
        self.firstInLine=self.queue[0]
        return True
        


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
        self.events=[]
        heqpq.heapify(self.events)
        self.servers=[]
        self.chosenServersHistory=[0,0]
      
        
        
    def createRequests(self):
        for t in range(self.timeOut):
            CurrentPossionResult=np.random.poisson(self.requestsRate)
            serverRates=np.random.poisson(self.serverRates)
           
            for CurReqIndex in range(CurrentPossionResult):
                req= Request(t+CurReqIndex/CurrentPossionResult)
                req.chosenServer=random.choices(list(range(len(self.probabilities))),weights=self.probabilities)[0] # note servers are indices from n to len(probabilities)-1
                req.serviceTime=1/serverRates[req.chosenServer]
                heqpq.heappush(self.events,(req.arrivalTime,req))
                

    def createServers(self):
        for serv in range(self.numOfServers):
            self.servers.append(Server(self.serverRates[serv], self.queues[serv]))


    def processRequests(self):
        sumRequestsAllTimes=0
        currentRequestNum= 0

        receivedService= 0
        thrownOut= 0
        lastRequest= 0
        sumWaitingTime=0
        sumServiceTime=0
        self.currentTime=0
        while self.events and self.currentTime <self.timeOut:
            _,req=heqpq.heappop(self.events)
            self.currentTime=req.arrivalTime
            lastRequest=req
            
            if self.servers[req.chosenServer].addRequest(req):
                receivedService += 1
                sumWaitingTime += (req.serviceEndTime - req.arrivalTime - 1/self.servers[req.chosenServer].rate)
                sumServiceTime += req.serviceTime
                
            else:
                thrownOut += 1
                currentRequestNum -= 1
                    
        Tw=sumWaitingTime/receivedService
        Ts=sumServiceTime/receivedService
        Tend=lastRequest.serviceEndTime

        strResult = "receivedService: " + str(receivedService) + " thrownOut: " + str(thrownOut)+ " Tend: " + str(Tend) + " Tw: " + str(Tw) + " Ts: " + str(Ts)
        return strResult
        
 
        
        
def main(argc):
    SimulatorTimeout = int(argc[0])
    numberOfServers = int(argc[1] )
    ServersProbabilities = [float(arg) for arg in argc[2:2+numberOfServers]]
    RequestsRate = int(argc[2+numberOfServers])
    Queues = [int(arg) for arg in argc[3+numberOfServers:3+2*numberOfServers]]
    ServersRates = [int(arg) for arg in argc[3+2*numberOfServers:]]
    Shimon = Simulator(SimulatorTimeout,numberOfServers, ServersProbabilities, RequestsRate, Queues, ServersRates)
    Shimon.createServers()
    Shimon.createRequests()
    result=Shimon.processRequests()
    print("Result- ",result)


if __name__ == "__main__":
    breakpoint()
    main(sys.argv[1:])   
    
'''
prompt : help me to implement in python load balancer that is event driven simulator

import heapq
from collections import deque
import random

class Server:
    def __init__(self, id):
        self.id = id
        self.busy_until = 0
        self.queue

class Request:
    def __init__(self, id, arrival_time, processing_time):
        self.id = id
        self.arrival_time = arrival_time
        self.processing_time = processing_time

class LoadBalancer:
    def __init__(self, num_servers):
        self.servers = [Server(i) for i in range(num_servers)]
        self.queue = deque()

    def add_request(self, request):
        self.queue.append(request)

    def process_request(self, current_time):
        if not self.queue:
            return None
        # choose server by probabilty and check if queue is full
        available_servers = [s for s in self.servers if s.busy_until <= current_time]
        if not available_servers:
            return None

        request = self.queue.popleft()
        server = min(available_servers, key=lambda s: s.busy_until)
        server.busy_until = current_time + request.processing_time
        return (request, server)

class Simulator:
    def __init__(self, num_servers, simulation_time):
        self.load_balancer = LoadBalancer(num_servers)
        self.events = []
        self.current_time = 0
        self.simulation_time = simulation_time

    def add_event(self, event_time, event_type, event_data):
        heapq.heappush(self.events, (event_time, event_type, event_data))

    def run(self):
        while self.events and self.current_time < self.simulation_time:
            self.current_time, event_type, event_data = heapq.heappop(self.events)

            if event_type == "arrival":
                self.load_balancer.add_request(event_data)
                self.add_event(self.current_time, "process", None)
            
            elif event_type == "process":
                result = self.load_balancer.process_request(self.current_time)
                if result:
                    request, server = result
                    print(f"Time {self.current_time}: Request {request.id} assigned to Server {server.id}")
                    self.add_event(self.current_time + request.processing_time, "complete", server)
                
            elif event_type == "complete":
                server = event_data
                print(f"Time {self.current_time}: Server {server.id} completed a request")
                self.add_event(self.current_time, "process", None)

# Example usage
sim = Simulator(num_servers=3, simulation_time=100)

# Generate some sample requests
for i in range(20): # for i in epoch (determined by T )
                        # for j in requests in each timestep (determined by lambada)
    arrival_time = random.randint(0, 90)
    processing_time = random.randint(5, 15)
    request = Request(i, arrival_time, processing_time)
    sim.add_event(arrival_time, "arrival", request)

sim.run()
'''